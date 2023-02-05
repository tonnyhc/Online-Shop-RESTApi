from django.urls import path

from OnlineShopBackEnd.shop_basket.views import BasketView

urlpatterns = [
    path('<str:user>/', BasketView.as_view(), name='basket_view')
]