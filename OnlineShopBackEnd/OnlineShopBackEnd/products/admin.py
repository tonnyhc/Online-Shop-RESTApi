from django.contrib import admin

from OnlineShopBackEnd.products.models import Product, ProductRating, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    exclude = ('ratings', )
    list_display = [
        'title', 'product_id', 'product_price', 'category', 'slug'
    ]

@admin.register(ProductRating)
class RatingAdmin(admin.ModelAdmin):
    pass
