from django.urls import path

from OnlineShopBackEnd.products.views import ProductsListView, ProductDetailsView, ProductRateView, \
    FavoriteProductsListView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products list'),
    path('favorites/', FavoriteProductsListView.as_view(), name='favorite products list'),
    path('<str:slug>/', ProductDetailsView.as_view(), name='product details'),
    path('<str:slug>/rate/', ProductRateView.as_view(), name='product rate'),
]