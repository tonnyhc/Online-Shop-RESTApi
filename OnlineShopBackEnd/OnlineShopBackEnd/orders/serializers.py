from django.contrib.auth import get_user_model
from rest_framework import serializers

from datetime import datetime

from OnlineShopBackEnd.orders.models import Order, OrderItem, DiscountCode
from OnlineShopBackEnd.products.serializers import ProductSerializerOrderDetails

UserModel = get_user_model()


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerOrderDetails()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ('code', 'discount')


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    discount = DiscountCodeSerializer()
    date_of_order = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'full_name', 'phone_number', 'email', 'town', 'address', 'post_code', 'items',
            'date_of_order', 'shipping_date', 'total_price', 'discounted_price', 'order_status', 'discount', 'id'
        )

    @staticmethod
    def get_date_of_order(obj):
        date_str = str(obj.order_date)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')

        formatted_date = date_obj.strftime('%d %B %Y, %H:%M')
        return formatted_date

    @staticmethod
    def get_email(obj):
        return obj.user.email

    @staticmethod
    def get_discount(obj):
        if not obj.discount:
            return

        order_discount = obj.discount
        try:
            discount = DiscountCode.objects.get(code=order_discount)
        except DiscountCode.DoesNotExist:
            return

        discount_code = discount.code
        discount_percentage = discount.discount
        return {
            'code': discount_code,
            'discount': discount_percentage
        }


class EditOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'town', 'address', 'post_code')


class ListOrdersSerializer(serializers.ModelSerializer):
    date_of_order = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'date_of_order', 'total_price', 'order_status', 'user_email', 'full_name']

    def get_date_of_order(self, obj):
        date_str = str(obj.order_date)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')

        formatted_date = date_obj.strftime('%d %B %Y, %H:%M')
        return formatted_date

    def get_user_email(self, obj):
        return obj.user.email



