from django.db import DatabaseError, IntegrityError
from rest_framework import generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import cloudinary.uploader

from OnlineShopBackEnd.admin_panel.serializer import AddProductSerializer
from OnlineShopBackEnd.admin_panel.serializers import DiscountCodeAdminSerializer
from OnlineShopBackEnd.admin_panel.utils import IsStaffPermission
from OnlineShopBackEnd.orders.models import Order, DiscountCode
from OnlineShopBackEnd.orders.serializers import ListOrdersSerializer, OrderDetailsSerializer, DiscountCodeSerializer
from OnlineShopBackEnd.products.models import Product, ProductImage, Category
from OnlineShopBackEnd.products.serializers import ProductSerializer, CategorySerializer


class GetCategories(rest_generic_views.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        final_list = []
        for category in self.queryset.all():
            final_list.append({
                'id': category.id,
                'category': category.category,
                'total_products': category.product_set.count(),
            })
        return Response(
            final_list, status=status.HTTP_200_OK)


class AddCategoryView(rest_generic_views.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        category_name = request.data.get('category')

        if self.queryset.filter(category=category_name):
            return Response({
                'message': "There is already a category with that name"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.create(category=category_name)
            category.save()
            return Response({
                'id': category.id,
                'category': category.category,
                'total_products': 0
            }, status=status.HTTP_200_OK)
        except DatabaseError:
            return Response({
                'message': 'A problem occured. Please try again!'
            }, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(rest_generic_views.DestroyAPIView):
    queryset = Category.objects.all()


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


class ProductsListView(rest_generic_views.ListAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProductView(rest_generic_views.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Product.objects.all()
    lookup_field = 'slug'


class EditProductView(rest_generic_views.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    parser_classes = [
        JSONParser,
        MultiPartParser,
    ]
    products_queryset = Product.objects.all()
    images_queryset = ProductImage.objects.all()
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        # TODO
        data = request.data
        a = 5


class OrdersListView(rest_generic_views.ListAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Order.objects.all()
    serializer_class = ListOrdersSerializer

    def get(self, request, *args, **kwargs):
        orders = self.queryset.order_by('-order_date')

        return Response(self.serializer_class(orders, many=True).data)


class OrderDetailsView(rest_generic_views.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer


class DiscountCodeListView(rest_generic_views.ListAPIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeAdminSerializer

class CreateDiscountCodeView(rest_generic_views.CreateAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeAdminSerializer
    list_serializer = DiscountCodeAdminSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        code = validated_data.get('code')
        discount = validated_data.get('discount')
        expiry_date = validated_data.get('expiry_date')

        discount_code = DiscountCode.objects.create(code=code, discount=discount, expiry_date=expiry_date)



        return Response(self.list_serializer(discount_code).data, status=status.HTTP_201_CREATED)



@api_view(('POST',))
@permission_classes([IsAuthenticated, IsStaffPermission])
@authentication_classes([TokenAuthentication])
def change_order_status(request, pk):
    requested_status = request.data['status']

    if not requested_status or requested_status == '':
        return Response({
            'message': "Please provide status for the order!"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.filter(pk=pk).get()
    except Order.DoesNotExist:
        return Response({
            'message': "The order you are trying to change does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        order.order_status = requested_status
        order.save()
        return Response({
            'message': "Order status updated successfully"
        }, status=status.HTTP_200_OK)
    except IntegrityError:
        return Response({
            "message": "The status you provided does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

