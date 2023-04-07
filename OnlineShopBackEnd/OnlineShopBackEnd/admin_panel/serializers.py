from django.contrib.auth import get_user_model
from rest_framework import serializers

from OnlineShopBackEnd.orders.models import DiscountCode
from OnlineShopBackEnd.products.models import Product


UserModel = get_user_model()

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('slug',)


class OrderAdminSerializer(serializers.ModelSerializer):
    class Meta:
        pass

class DiscountCodeAdminSerializer(serializers.ModelSerializer):
    times_used = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    expiry_date = serializers.SerializerMethodField()

    class Meta:
        model = DiscountCode
        fields = ('code', 'discount', 'times_used', 'total_income', 'expiry_date')

    @staticmethod
    def get_times_used(obj):
        orders = obj.order_set.count()
        return orders

    @staticmethod
    def get_expiry_date(obj):
        return obj.expiry_date if obj.expiry_date else 'Eternal'

    @staticmethod
    def get_total_income(obj):
        orders = obj.order_set.all()
        order_prices = []
        for order in orders:
            price = order.discounted_price if order.discounted_price else order.total_price
            order_prices.append(price)
        return sum(order_prices)


class DiscountCodeCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ('code', 'discount', 'expiry_date')


class UserModelSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'full_name','gender', 'total_orders', 'total_income')

    @staticmethod
    def get_total_orders(obj):
        return obj.order_set.count()

    @staticmethod
    def get_total_income(obj):
        orders = obj.order_set.all()
        return sum([order.discounted_price or order.total_price for order in orders])


