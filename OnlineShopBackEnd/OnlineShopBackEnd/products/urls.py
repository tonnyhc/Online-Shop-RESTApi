from django.urls import path

from OnlineShopBackEnd.products.views import ProductsListView, ProductDetailsView, ProductRateView, \
    FavoriteProductsListView, FavoriteProductsRemoveView, FavoriteProductsCreateView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products list'),
    path('favorites/', FavoriteProductsListView.as_view(), name='favorite products list'),
    path('favorites/<str:slug>/remove/', FavoriteProductsRemoveView.as_view(), name='favorite products remove'),
    path('favorites/<str:slug>/add/', FavoriteProductsCreateView.as_view(), name='favorite products add'),
    path('<str:slug>/', ProductDetailsView.as_view(), name='product details'),
    path('<str:slug>/rate/', ProductRateView.as_view(), name='product rate'),
]