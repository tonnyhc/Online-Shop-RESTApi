from django.urls import path

from OnlineShopBackEnd.orders.views import CreateOrder

urlpatterns = [
    path('create/', CreateOrder.as_view(), name='create order'),

]