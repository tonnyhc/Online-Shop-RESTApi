from rest_framework import serializers

from OnlineShopBackEnd.orders.models import DiscountCode
from OnlineShopBackEnd.products.serializers import ProductImageSerializer
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
        image = obj.product.productimage_set.all()[0]
        return ProductImageSerializer(image).data

    @staticmethod
    def get_slug(obj):
        return obj.product.slug

    @staticmethod
    def get_discounted_price(obj):
        return obj.product.discounted_price


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ('code', 'discount')


class BasketSerializer(serializers.ModelSerializer):
    basketitem_set = BasketItemSerializer(many=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'user', 'created_at', 'updated_at', 'basketitem_set', 'discounted_price', 'discount']

    def get_discount(self, obj):
        try:
            code = DiscountCode.objects.filter(code=obj.discount_code).get()
            return DiscountCodeSerializer(code).data
        except DiscountCode.DoesNotExist:
            pass

class CreateBasketItemAndAddToBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['basket', 'product', 'quantity']
