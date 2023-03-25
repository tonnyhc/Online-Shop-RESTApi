from rest_framework import generics as rest_generic_views
from rest_framework.permissions import IsAuthenticated

from OnlineShopBackEnd.admin_panel.utils import IsStaffPermission
from OnlineShopBackEnd.orders.models import Order


class GetDashboardView(rest_generic_views.ListAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Order.objects.all()

