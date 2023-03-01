from django.urls import path

from OnlineShopBackEnd.products.views import ProductsListView, ProductDetailsView, ProductRateView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products list'),
    path('<str:slug>/', ProductDetailsView.as_view(), name='product details'),
    path('<str:slug>/rate/', ProductRateView.as_view(), name='product rate'),
]