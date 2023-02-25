from rest_framework import serializers

from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem


class BasketItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'date_added', 'subtotal']


class BasketSerializer(serializers.ModelSerializer):
    basketitem_set = BasketItemSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_ordered', 'order_date', 'basketitem_set']


class CreateBasketItemAndAddToBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['basket', 'product', 'quantity']
