from django.urls import path

from OnlineShopBackEnd.shop_basket.views import BasketView, CreateBasketItemAndAddToBasket, RemoveBasketItemFromBasket

urlpatterns = [
    path('<str:user>/', BasketView.as_view(), name='basket view'),
    path('add-to-basket/<str:slug>/', CreateBasketItemAndAddToBasket.as_view(), name='add item to basket'),
    path('remove-from-basket/<str:slug>/', RemoveBasketItemFromBasket.as_view(), name='remove item from basket')
]