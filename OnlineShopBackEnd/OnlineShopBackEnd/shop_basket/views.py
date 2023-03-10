from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics as rest_generic_views, views as rest_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
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
            basket = self.queryset.get(user=self.request.user)
            return basket

        except Basket.DoesNotExist:
            basket = self.queryset.create(user=self.request.user)
            return basket


class CreateBasketItemAndAddToBasket(rest_generic_views.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
            basket = Basket.objects.filter(user=request.user).get()
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=request.user)

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
    permission_classes = [IsAuthenticated]

    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            basket = Basket.objects.get(user=request.user)
            product = Product.objects.get(slug=self.request.data['product'])
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
    in the Headers
    """


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_basket_item_quantity(request, slug):
    user = request.user
    basket = Basket.objects.get(user=user)

    try:
        basket_item = BasketItem.objects.filter(basket=basket, product__slug=slug).get()
    except BasketItem.DoesNotExist:
        return Response({
            'message': "Can't update quantity as the basket item seems not to exist!"
        })

    try:
        action = request.data.get('action').split(' ')[0]
        value = int(request.data.get('action').split(' ')[1])
        if action == "+":
            basket_item.quantity += value
        elif action == '-' and basket_item.quantity > 1:
            basket_item.quantity -= value
        basket_item.save()
    except Exception:
        return Response({
            'message': "An error occurred please try again later."
        })

    serializer = BasketItemSerializer(basket_item)

    return Response({
        'basket_item': serializer.data
    })
