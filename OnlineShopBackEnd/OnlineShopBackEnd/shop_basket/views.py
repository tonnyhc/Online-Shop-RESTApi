from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken import models as authtoken_models

from OnlineShopBackEnd.products.models import Product
from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem
from OnlineShopBackEnd.shop_basket.serializers import BasketSerializer, CreateBasketItemAndAddToBasketSerializer, \
    BasketItemSerializer

UserModel = get_user_model()


class BasketView(rest_generic_views.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]

    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_field = 'user'

    def get_object(self):
        try:
            token = self.request.headers.get("Authorization").split(' ')[1]
            request_user = authtoken_models.Token.objects.get(key=token).user
            basket = self.queryset.get(user=request_user)
            return basket

        except Basket.DoesNotExist:
            basket = self.queryset.create(user=self.request.user)
            return basket


class CreateBasketItemAndAddToBasket(rest_generic_views.CreateAPIView):
    authentication_classes = [TokenAuthentication]

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
            # request_user = UserModel.objects.filter(username=request.data['user']).get()
            token = self.request.headers.get('Authorization').split(' ')[1]
            request_user = authtoken_models.Token.objects.get(key=token).user
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

        serializer = self.get_serializer(basket_item)

        return Response({
            'item': serializer.data,
            'message': "Product successfully added to basket"
        }, status=status.HTTP_201_CREATED)


class RemoveBasketItemFromBasket(rest_generic_views.DestroyAPIView):
    authentication_classes = [TokenAuthentication]

    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()


    def destroy(self, request, *args, **kwargs):
        try:
            token = self.request.headers.get('Authorization').split(' ')[1]
            request_user = authtoken_models.Token.objects.get(key=token).user
            basket = Basket.objects.get(user=request_user)
            product = Product.objects.get(slug=self.request.data['product'])
            print(self.queryset.get(basket=basket, product=product))
            item = self.queryset.get(basket=basket, product=product)

            self.perform_destroy(item)
            return Response({
                'message': "Product deleted from basket successfully!"
            })
        except ObjectDoesNotExist:
            return Response({
                'message': "There was a problem deleting the product from your basket!"
            })
    """
    This view expects a 'DELETE' method with body 
    {
        'product': <product_slug>
    }
    and must include the user token
    and the csrf_token
    """
