from django.urls import path

from OnlineShopBackEnd.shop_basket.views import BasketView, CreateBasketItemAndAddToBasket, RemoveBasketItemFromBasket, \
    update_basket_item_quantity, apply_discount_code, remove_discount_code

urlpatterns = [
    path('apply-discount/', apply_discount_code, name='apply discount code'),
    path('remove-discount/', remove_discount_code, name='remove discount code'),
    path('add-to-basket/<str:slug>/', CreateBasketItemAndAddToBasket.as_view(), name='add item to basket'),
    path('remove-from-basket/<str:slug>/', RemoveBasketItemFromBasket.as_view(), name='remove item from basket'),
    path('update-quantity/<str:slug>/', update_basket_item_quantity, name='update basket item quantity'),
    path('<str:user>/', BasketView.as_view(), name='basket view'),
]

