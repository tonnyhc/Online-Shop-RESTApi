from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
from django.utils import timezone

from OnlineShopBackEnd.products.models import Product

UserModel = get_user_model()


class Basket(models.Model):
    MAX_LEN_DISCOUNT_CODE = 50
    MIN_LEN_DISCOUNT_CODE = 3

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discounted_price = models.FloatField(null=True, blank=True)
    discount_code = models.CharField(
        max_length=MAX_LEN_DISCOUNT_CODE,
        validators=[validators.MinLengthValidator(MIN_LEN_DISCOUNT_CODE)],
        blank=True,
        null=True
    )

    def total_cost(self):
        return sum(item.total_cost() for item in self.basketitem_set.all())

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
