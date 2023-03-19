from django.contrib.auth import get_user_model
from django.db.models import Q, Avg
from rest_framework import exceptions as rest_exceptions, generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from OnlineShopBackEnd.products.models import Product, ProductRating, Category, FavoriteProducts
from OnlineShopBackEnd.products.serializers import ProductSerializer, ProductRatingSerializer, CategorySerializer, \
    FavoriteProductsSerializer

UserModel = get_user_model()


class ProductsListView(rest_generic_views.ListAPIView):
    queryset = Product.objects.annotate(avg_rating=Avg('ratings__score'))
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        search_query = params.get('search', None)
        brands = params.get('brands')
        model = params.get('model')
        min_price = params.get('min-price')
        max_price = params.get('max-price')
        category_filter = params.get('category')
        average_rating = params.get('average-rating')
        gender = params.get('gender')

        try:
            min_price = float(min_price)
        except (TypeError, ValueError):
            min_price = None

        try:
            max_price = float(max_price)
        except (TypeError, ValueError):
            max_price = None

        if search_query and search_query != '':
            filtered_queryset = []
            for product in self.queryset.all():
                product_str = f'{product.brand} {product.model}'
                if search_query.lower() in product_str.lower():
                    filtered_queryset.append(product)
            queryset = filtered_queryset

        if brands and ',' in brands:
            q_object = Q()
            for brand in brands:
                q_object |= Q(brand=brand)
            queryset.filter(q_object)
        elif brands:
            queryset = queryset.filter(brand=brands)

        if model:
            queryset = queryset.filter(model=model)
        if min_price:
            queryset = queryset.filter(product_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(product_price__lte=max_price)
        # Category filter
        if category_filter and ',' in category_filter:
            q_object = Q()
            category_filter = category_filter.split(',')
            for category_str in category_filter:
                try:
                    category = Category.objects.get(category=category_str)
                except Category.DoesNotExist:
                    return
                q_object |= Q(category=category)
            queryset = queryset.filter(q_object)
        elif category_filter:
            try:
                category = Category.objects.get(category=category_filter)
            except Category.DoesNotExist:
                return
            queryset = queryset.filter(category=category)

        if average_rating:
            queryset = queryset.filter(avg_rating__gte=float(average_rating))

        if gender and ',' in gender:
            q_object = Q()
            gender = gender.split(',')
            for g in gender:
                q_object |= Q(gender=g)

            queryset = queryset.filter(q_object)
        elif gender:
            queryset = queryset.filter(gender=gender)

        products = queryset
        categories = Category.objects.filter(product__in=products).distinct()

        for product in products:
            ratings = product.ratings.all()
            scores = [rating.score for rating in ratings]
            product.average_rating = sum(scores) / len(scores) if scores else None
        serializer = ProductSerializer(products, many=True)

        return serializer.data

    def get_filters(self):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        brands = Product.objects.values_list('brand', flat=True).distinct()
        data = {
            'categories': serializer.data,
            'brands': brands
        }
        return data

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        filters = self.get_filters()
        data = {
            'products': products,
            'query_filters': filters,
        }
        return Response(data)


class ProductDetailsView(rest_generic_views.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductRateView(rest_generic_views.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductRatingSerializer

    def perform_create(self, serializer):
        rating_data = self.request.data
        product_slug = self.kwargs.get('slug')

        # Checking if the product exists in DB otherwise raises ValidationError
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            error_message = {"message": "Can not give rating to a product because the product does not exist!"}
            raise rest_exceptions.ValidationError(error_message, code=status.HTTP_400_BAD_REQUEST)

        # Checking if the user is rated the same product, if so raises ValidationError
        if ProductRating.objects.filter(user=self.request.user, products=product).exists():
            error_message = {"message": "Can not give rating to a product because that user has already rated it!"}
            raise rest_exceptions.ValidationError(error_message, code=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        rating = serializer.save(user=self.request.user)
        rating.products.add(product)
        # This is only a post request that requires data in the following format:
        # {
        #     "score": "{0 to 5 delimiter 0.5}"
        # }


class FavoriteProductsListView(rest_generic_views.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FavoriteProductsSerializer

    def get_queryset(self):
        products = FavoriteProducts.objects.filter(user=self.request.user).all()
        return products


