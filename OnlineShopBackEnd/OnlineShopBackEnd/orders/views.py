from rest_framework import generics as rest_generic_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from OnlineShopBackEnd.orders.models import Order, OrderItem
from OnlineShopBackEnd.orders.serializers import CreateOrderSerializer, ListOrdersSerializer, OrderDetailsSerializer, \
    EditOrderSerializer
from OnlineShopBackEnd.products.models import Product
from OnlineShopBackEnd.shop_basket.models import Basket


class CreateOrder(rest_generic_views.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    # TODO: when order is created must reduce the quantity of every single item
    def post(self, request, *args, **kwargs):
        order = Order.objects.create(
            user=request.user,
            full_name=request.data.get('full_name'),
            phone_number=request.data.get('phone_number'),
            town=request.data.get('town'),
            address=request.data.get('address'),
            post_code=request.data.get('post_code'),
        )

        items = request.data.get('items')
        print(items)
        item_objects = []
        for item in items:
            try:
                product = Product.objects.get(slug=item['slug'])
            except Product.DoesNotExist:
                return Response({
                    "Can not create order as some of the products do not exist!"
                })

            order_item = OrderItem(
                product=product,
                quantity=int(item['quantity']),
                price=(product.discounted_price if product.discounted_price else product.product_price),
                order=order
            )
            item_objects.append(order_item)

        OrderItem.objects.bulk_create(item_objects)
        order.total_price = sum(item.price for item in item_objects)
        order.save()

        basket = Basket.objects.get(user=request.user)
        basket.delete()

        serializer = self.get_serializer(order)

        return Response({
            "order": serializer.data
        })

    """
    The view expects data like the following
    {
    "full_name": "<full_name>",
    "phone_number": "<phone_number>",
    "town": "<town>",
    "address": "<address>",
    "post_code": "<post_code>",
    "items": [
        {
            "slug": "<product_slug>",
            "quantity": "<quantity>"
        }
    ]
}
    """


class OrdersList(rest_generic_views.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = ListOrdersSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = self.queryset.filter(user=user)

        return Response(self.serializer_class(orders, many=True).data)


class OrderDetails(rest_generic_views.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            order = self.queryset.filter(pk=kwargs['pk']).get()
        except Order.DoesNotExist:
            return Response({
                'message': "The order you are trying to view seems to not exist. You can contact us if this is a problem for you!"
            }, status=status.HTTP_404_NOT_FOUND)

        if order.user.pk != request.user.pk:
            return Response({
                "message": "You can only view your own orders"
            }, status=status.HTTP_403_FORBIDDEN)
        return self.retrieve(self, request, *args, **kwargs)


class EditOrder(rest_generic_views.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = EditOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        order = self.queryset.filter(pk=kwargs['pk']).first()
        if order.user.pk != request.user.pk:
            return Response({
                'message': "You can only edit your own orders"
            }, status=status.HTTP_403_FORBIDDEN)
        if order.order_status != 'InPreparation':
            return Response({
                'message': "You can not edit your order, it is already shipped"
            })
        else:
            return self.update(request, *args, **kwargs)


class DeleteOrder(rest_generic_views.DestroyAPIView):
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        order = self.queryset.filter(pk=kwargs['pk']).first()
        user = request.user
        if order.user != user:
            return Response({
                'message': "You can't delete orders that are not yours"
            }, status=status.HTTP_403_FORBIDDEN)

        if order.order_status != "InPreparation":
            return Response({
                'message': "You can't cancel your order! It is already shipped."
            }, status=status.HTTP_400_BAD_REQUEST)
        self.destroy(request, *args, **kwargs)
        return Response({
            "message": "You have successfully canceled your order",
        }, status=status.HTTP_204_NO_CONTENT)
