from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics as rest_generic_views
from rest_framework.response import Response

from OnlineShopBackEnd.products.models import Product
from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem
from OnlineShopBackEnd.shop_basket.serializers import BasketSerializer, CreateBasketItemAndAddToBasketSerializer

UserModel = get_user_model()


class BasketView(rest_generic_views.RetrieveAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_field = 'user'

    def get_object(self):
        user = self.request.user
        return self.queryset.get(user=user)


class CreateBasketItemAndAddToBasket(rest_generic_views.CreateAPIView):
    queryset = BasketItem.objects.all()
    basket = Basket.objects.all()
    serializer_class = CreateBasketItemAndAddToBasketSerializer

    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.filter(slug=request.data['product']).get()
        except Product.DoesNotExist:
            return Response({
                "message": "The product you are trying to add to your basket does not exist!"
            })

        try:
            request_user = UserModel.objects.filter(username=request.data['user']).get()
        except ObjectDoesNotExist:
            return Response({
                'message': "The user does not exist"
            })

        try:
            basket = Basket.objects.filter(user=request_user).get()
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=request_user)

        try:
            basket_item = BasketItem.objects.filter(product=product, basket=basket).get()
            basket_item.quantity += int(request.data['quantity'])
            basket_item.save()
        except BasketItem.DoesNotExist:
            basket_item = BasketItem.objects.create(
                product=product,
                quantity=request.data['quantity'],
                basket=basket,
            )

        return Response({
            'message': "Product successfully added to basket"
        })
