from django.contrib.auth import get_user_model
from rest_framework import generics as rest_generic_views
from OnlineShopBackEnd.shop_basket.models import Basket
from OnlineShopBackEnd.shop_basket.serializers import BasketSerializer

UserModel = get_user_model()

class BasketView(rest_generic_views.RetrieveAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_field = 'user'
    def get_object(self):
        user = self.request.user
        return self.queryset.get(user=user)




