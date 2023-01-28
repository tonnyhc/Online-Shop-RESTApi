from django.contrib import admin

from OnlineShopBackEnd.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'product_id', 'product_price', 'category'
    ]
