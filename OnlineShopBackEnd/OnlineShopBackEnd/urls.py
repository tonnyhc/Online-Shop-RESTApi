from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('OnlineShopBackEnd.shop_basket.urls')),
    path('accounts/', include('OnlineShopBackEnd.accounts.urls')),
    path('products/', include('OnlineShopBackEnd.products.urls')),
    path('basket/', include('OnlineShopBackEnd.shop_basket.urls')),
]
