from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics as rest_generic_views, views as rest_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken import models as authtoken_models

from OnlineShopBackEnd.orders.models import DiscountCode
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
def apply_discount_code(request):
    code = request.data.get('code')

    try:
        user = request.user
    except ObjectDoesNotExist:
        return Response({
            "message": "User does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist:
        return Response({
            'message': "Basket does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    if not code:
        return Response({
            "message": "Please provide a discount code in order to get a discount!"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        discount = DiscountCode.objects.filter(code=code).get()
    except DiscountCode.DoesNotExist:
        return Response({
            "message": "The code is not valid!"
        }, status=status.HTTP_400_BAD_REQUEST)

    discount_percentage = discount.discount
    # Malking calculation for the total cost of the basket
    basket_cost = sum((item.subtotal() for item in basket.basketitem_set.all()))
    discounted_cost = basket_cost - (basket_cost * (int(discount_percentage) / 100))
    basket.discounted_price = discounted_cost
    basket.discount_code = code
    basket.save()
    return Response({
        'discounted_price': discounted_cost,
        'discount': {
            'code': discount.code,
            'discount': discount.discount
        }
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_discount_code(request):
    try:
        user = request.user
    except ObjectDoesNotExist:
        return Response({
            "message": "User does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist:
        return Response({
            'message': "Basket does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    basket.discounted_price = None
    basket.discount_code = None
    basket.save()
    return Response({
        'message': "Discount code successfully removed"
    }, status=status.HTTP_200_OK)


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
        }, status=status.HTTP_400_BAD_REQUEST)

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
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = BasketItemSerializer(basket_item)

    return Response({
        'basket_item': serializer.data
    }, status=status.HTTP_200_OK)
