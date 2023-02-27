from django.contrib.auth import get_user_model
from rest_framework import exceptions as rest_exceptions, generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from OnlineShopBackEnd.products.models import Product, ProductRating
from OnlineShopBackEnd.products.serializers import ProductSerializer, ProductRatingSerializer

UserModel = get_user_model()


class ProductsListView(rest_generic_views.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        products = queryset
        for product in products:
            ratings = product.ratings.all()
            scores = [rating.score for rating in ratings]
            product.average_rating = sum(scores) / len(scores) if scores else None
            print(product)
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

        #Checking if the product exists in DB otherwise raises ValidationError
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            error_message = {"message": "Can not give rating to a product because the product does not exist!"}
            raise rest_exceptions.ValidationError(error_message, code=status.HTTP_400_BAD_REQUEST)

        #Checks if the user exists otherwise or the user is logged in otherwise raises ValidationError
        #TODO: check if the user is logged in
        # try:
        #     user = UserModel.objects.get(username=rating_data['user'])
        # except UserModel.DoesNotExist:
        #     error_message = {
        #         "message": "Can not give rating to a product because that user does not exist or is not logged in!"}
        #     raise rest_exceptions.ValidationError(error_message, code=status.HTTP_400_BAD_REQUEST)

        #Checking if the user is rated the same product, if so raises ValidationError
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
