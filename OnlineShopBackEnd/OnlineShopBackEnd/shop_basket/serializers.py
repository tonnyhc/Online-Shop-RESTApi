from rest_framework import serializers

from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem


class BasketItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    product_price = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = [
            'id', 'product', 'product_price', 'discounted_price',
            'quantity', 'image', 'date_added', 'subtotal', 'slug'
        ]

    @staticmethod
    def get_product_price(obj):
        return obj.product.product_price

    @staticmethod
    def get_image(obj):
        return obj.product.image

    @staticmethod
    def get_slug(obj):
        return obj.product.slug

    @staticmethod
    def get_discounted_price(obj):
        return obj.product.discounted_price


class BasketSerializer(serializers.ModelSerializer):
    basketitem_set = BasketItemSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_ordered', 'order_date', 'basketitem_set']


class CreateBasketItemAndAddToBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['basket', 'product', 'quantity']
