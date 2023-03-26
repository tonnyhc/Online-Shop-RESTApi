from rest_framework import serializers

from datetime import datetime

from OnlineShopBackEnd.orders.models import Order, OrderItem
from OnlineShopBackEnd.products.serializers import ProductSerializerOrderDetails


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerOrderDetails()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    date_of_order = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'full_name', 'phone_number', 'town', 'address', 'post_code', 'items',
            'date_of_order', 'shipping_date', 'total_price', 'order_status', 'id'
        )

    def get_date_of_order(self, obj):
        date_str = str(obj.order_date)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')

        formatted_date = date_obj.strftime('%d %B %Y, %H:%M')
        return formatted_date


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

