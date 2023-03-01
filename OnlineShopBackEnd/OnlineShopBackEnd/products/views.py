from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import exceptions as rest_exceptions, generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from OnlineShopBackEnd.products.models import Product, ProductRating, Category
from OnlineShopBackEnd.products.serializers import ProductSerializer, ProductRatingSerializer

UserModel = get_user_model()


class ProductsListView(rest_generic_views.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.query_params.get('brand')
        model = self.request.query_params.get('model')
        min_price = self.request.query_params.get('min-price')
        max_price = self.request.query_params.get('max-price')
        category_filter = self.request.query_params.get('category')
        average_rating = self.request.query_params.get('average-rating')

        try:
            min_price = float(min_price)
        except (TypeError, ValueError):
            min_price = None

        try:
            max_price = float(max_price)
        except (TypeError, ValueError):
            max_price = None

        if brand:
            queryset = queryset.filter(brand=brand)
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
            queryset = queryset.filter(average_rating=average_rating)

        products = queryset

        for product in products:
            ratings = product.ratings.all()
            scores = [rating.score for rating in ratings]
            product.average_rating = sum(scores) / len(scores) if scores else None
        return products


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
