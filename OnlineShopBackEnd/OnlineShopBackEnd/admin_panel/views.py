
from rest_framework import generics as rest_generic_views, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import cloudinary.uploader

from OnlineShopBackEnd.admin_panel.serializer import AddProductSerializer
from OnlineShopBackEnd.admin_panel.utils import IsStaffPermission
from OnlineShopBackEnd.orders.models import Order
from OnlineShopBackEnd.orders.serializers import ListOrdersSerializer
from OnlineShopBackEnd.products.models import Product, ProductImage, Category


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


class AddProductView(rest_generic_views.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    serializer_class = AddProductSerializer
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    def post(self, request, *args, **kwargs):
        data = request.data
        brand = data.get('brand')
        model = data.get('model')
        product_id = data.get('product_id')
        category = data.get('category')
        price = data.get('product_price')
        gender = data.get('gender')

        images = request.FILES.getlist('images')
        try:
            category = Category.objects.filter(category=category).get()
        except Category.DoesNotExist:
            return Response({
                'message': "Please choose existing category, or create a new one"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.create(
                brand=brand,
                model=model,
                product_id=product_id,
                category=category,
                product_price=price,
                gender=gender
            )
        except Exception as e:
            print(e)
            return Response({
                'message': "Error"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            for image in images:
                image = ProductImage.objects.create(
                    product=product,
                    image=image
                )
                image.save()
        except Exception as e:
            return Response({
                'message': "Error in image"
            }, status=status.HTTP_400_BAD_REQUEST)

        product.save()
        return Response({
            'message': "Product added successfully"
        }, status=status.HTTP_200_OK)

    a = 5




