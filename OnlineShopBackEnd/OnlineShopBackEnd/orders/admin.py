from django.contrib import admin

from OnlineShopBackEnd.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
