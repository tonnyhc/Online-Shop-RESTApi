from django.urls import path

from OnlineShopBackEnd.admin_panel.views import GetDashboardView, AddProductView

urlpatterns = (
    path('dashboard/', GetDashboardView.as_view(), name='dashboard view'),
    path('add-product/', AddProductView.as_view(), name='add product'),
)
