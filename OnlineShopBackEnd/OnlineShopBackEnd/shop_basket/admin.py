from django.contrib import admin

from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'basket' , 'date_added',
    ]

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'user', 'is_ordered', 'order_date',
    ]