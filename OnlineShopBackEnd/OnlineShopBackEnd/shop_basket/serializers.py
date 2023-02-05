from rest_framework import serializers

from OnlineShopBackEnd.shop_basket.models import Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"