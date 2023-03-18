from django.contrib import admin

from OnlineShopBackEnd.orders.models import Order, DiscountCode


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(DiscountCode)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'expiry_date']
