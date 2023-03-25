from django.urls import path

from OnlineShopBackEnd.admin_panel.views import GetDashboardView

urlpatterns = (
    path('dashboard/', GetDashboardView.as_view(), name='dashobard view'),
)