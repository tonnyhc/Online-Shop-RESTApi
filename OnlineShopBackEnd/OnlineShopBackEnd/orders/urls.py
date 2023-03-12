from django.urls import path

from OnlineShopBackEnd.orders.views import CreateOrder, OrdersList, OrderDetails, EditOrder, DeleteOrder

urlpatterns = [
    path('', OrdersList.as_view(), name='list orders'),
    path('details/<int:pk>/', OrderDetails.as_view(), name='details order'),
    path('edit/<int:pk>/', EditOrder.as_view(), name='edit order'),
    path('delete/<int:pk>/', DeleteOrder.as_view(), name='delete order'),
    path('create/', CreateOrder.as_view(), name='create order'),

]