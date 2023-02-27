from rest_framework import generics as rest_generic_views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from OnlineShopBackEnd.orders.models import Order, OrderItem
from OnlineShopBackEnd.orders.serializers import CreateOrderSerializer
from OnlineShopBackEnd.products.models import Product


class CreateOrder(rest_generic_views.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

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
