from django.urls import path

from OnlineShopBackEnd.shop_basket.views import basket_view

urlpatterns = [
    path('', basket_view, name='basket_view')
]