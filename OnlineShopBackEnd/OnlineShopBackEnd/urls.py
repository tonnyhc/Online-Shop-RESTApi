from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('accounts/', include('OnlineShopBackEnd.accounts.urls')),
        path('products/', include('OnlineShopBackEnd.products.urls')),
        path('basket/', include('OnlineShopBackEnd.shop_basket.urls')),
        path('orders/', include('OnlineShopBackEnd.orders.urls')),
        path('admin-panel/', include('OnlineShopBackEnd.admin_panel.urls')),
    ]))
]
