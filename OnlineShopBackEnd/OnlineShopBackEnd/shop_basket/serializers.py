from rest_framework import serializers

from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"


class CreateBasketItemAndAddToBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = "__all__"