from django.contrib import admin

from OnlineShopBackEnd.products.models import Product, ProductRating, Category, FavoriteProducts, ProductImage


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [ProductImageInline]
    exclude = ('ratings',)
    list_display = [
        'brand', 'model', 'product_id', 'product_price', 'category', 'slug'
    ]


@admin.register(ProductRating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(FavoriteProducts)
class FavoriteProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ImageAdmin(admin.ModelAdmin):
    pass
