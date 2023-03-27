from rest_framework import serializers

from OnlineShopBackEnd.products.models import Product


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('slug',)
