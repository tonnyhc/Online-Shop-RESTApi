from rest_framework import generics as rest_generic_views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from OnlineShopBackEnd.admin_panel.utils import IsStaffPermission
from OnlineShopBackEnd.orders.models import Order
from OnlineShopBackEnd.orders.serializers import ListOrdersSerializer
from OnlineShopBackEnd.products.models import Product


class GetDashboardView(rest_generic_views.ListAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    order_serializer = ListOrdersSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        total_sales = sum([order.total_price for order in self.queryset.all()])
        total_orders = self.queryset.count()
        total_products = Product.objects.count()
        orders = []
        for order in self.queryset.all().order_by('-order_date'):
            orders.append(self.order_serializer(order).data)

        return Response({
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_products': total_products,
            'orders': orders,
        })




