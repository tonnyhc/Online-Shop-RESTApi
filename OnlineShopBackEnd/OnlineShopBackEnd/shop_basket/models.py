from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
from django.utils import timezone

from OnlineShopBackEnd.products.models import Product

UserModel = get_user_model()


class BasketException(Exception):
    """Capture basket related exceptions"""

# class Basket(models.Model):
#     """Stores a user's current basket, transitioning when an order is placed"""
#     IN_PROGRESS = 1
#     PROCESSED = 2
#     BASKET_STATUS = (
#         (IN_PROGRESS, "Open"),
#         (PROCESSED, 'Processed')
#     )
#
#     user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#     )
#     status = models.IntegerField(
#         choices=BASKET_STATUS,
#         default=IN_PROGRESS
#     )
#     created_date = models.DateField(
#         auto_now_add=True,
#     )
#
#     def count(self):
#         """Return total number of items in basket"""
#         count = self.basketitem_set.aggregate(
#             count=models.Sum('quantity'))['count']
#         if count is None:
#             count = 0
#         return count
#
#     def total(self):
#         """Return total price for the basket"""
#         products = self.basketitem_set.all().values_list('product_id', 'quantity')
#         total = 0
#
#         if products:
#             for product in products:
#                 product_id = product[0]
#                 quantity = product[1]
#                 price = Product.objects.get(pk=product_id).product_price
#
#                 total += quantity * price
#
#         return total
#
#     def create_order(self, order_details, stripe_id=None):
#         """Convert active basket into an order in the checkout app"""
#         #check if the user exists
#         items = self.basketitem_set.all()
#         number_of_items = items.count()
#         user = self.user
#
#         if not user:
#             #called with no user
#             raise BasketException(
#                 "Order cannot be generated as there is no associated user."
#             )
#         if not number_of_items:
#             #called with no items in basket
#             raise BasketException(
#                 "Order cannot be generated as the basket is empty."
#             )
#         if not stripe_id:
#             # stripe_id is confirmation of payment, required field
#             raise BasketException(
#                 "Order cannot be generated as there was a problem"
#                 "identifying the payment."
#             )
#
#         #create order
#         order_data = {
#             'user':user,
#             #billing data is populated from user profile
#             'billing_name': f'{user.first_name} {user.last_name}',
#             'billing_address': user.address,
#             'billing_city': user.city,
#             'billing_post_code': user.post_code,
#             # user can add shipping information if different from billing
#             'shipping_name': order_details.get('shipping_name'),
#             'shiping_address': order_details.get('shipping_adress'),
#             'shipping_city': order_details.get("shipping_city"),
#             'shipping_post_code': order_details.get("shipping_post_code"),
#             #store stripe payment id
#             'stripe_id': stripe_id,
#         }
#
#         order = Order.objects.create(**order_data)
#         # TODO change paid to create
#         order.status = Order.PAID
#         order.save()


class Basket(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)

    def total_cost(self):
        return sum(item.total_cost() for item in self.basketitem_set.all())


    def order(self):
        self.is_ordered = True
        self.order_date = timezone.now()
        self.save()

    def __str__(self):
        return f'Basket {self.id}'


# TODO: when user adds item to basket must save its quantity for no more that 5 minutes!
class BasketItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            validators.MinValueValidator(1),
        ]
    )
    date_added = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Item total: {self.quantity * self.product.product_price} (Quantity :{self.quantity}\
        , Price: {self.product.product_price}  - Product: {self.product.brand} {self.product.model})"

    def subtotal(self):
        if self.product.discounted_price:
            total = self.product.discounted_price * self.quantity
        else:
            total = self.quantity * self.product.product_price

        if total is None:
            total = 0

        return total
