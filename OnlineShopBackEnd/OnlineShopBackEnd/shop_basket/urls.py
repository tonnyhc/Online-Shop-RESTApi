from django.urls import path

from OnlineShopBackEnd.shop_basket.views import BasketView, CreateBasketItemAndAddToBasket

urlpatterns = [
    path('<str:user>/', BasketView.as_view(), name='basket view'),
    path('add-to-basket/<str:slug>/', CreateBasketItemAndAddToBasket.as_view(), name='add item to basket')
]