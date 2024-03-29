from datetime import datetime

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from OnlineShopBackEnd.orders.mixins import OrderStatusEnumMixin
from OnlineShopBackEnd.products.models import Product

UserModel = get_user_model()


class DiscountCode(models.Model):
    MAX_LEN_CODE = 25
    MIN_LEN_CODE = 3
    code = models.CharField(
        unique=True,
        max_length=MAX_LEN_CODE,
        validators=[validators.MinLengthValidator(MIN_LEN_CODE)]
    )
    discount = models.IntegerField()

    expiry_date = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.code


class Order(models.Model):
    MAX_LEN_FULL_NAME = 120
    MAX_LEN_PHONE_NUMBER = 10
    MIN_LEN_PHONE_NUMBER = 10
    MAX_LEN_TOWN_NAME = 50
    MIN_LEN_TOWN_NAME = 3
    MAX_LEN_ADDRESS = 100
    MIN_LEN_ADDRESS = 3
    MAX_LEN_POST_CODE = 5
    MIN_LEN_POST_CODE = 4
    MAX_DIGIT_TOTAL_PRICE = 10

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        blank=False,
        null=False,
        max_length=MAX_LEN_FULL_NAME
    )

    phone_number = models.CharField(
        blank=False,
        null=False,
        max_length=MAX_LEN_PHONE_NUMBER,
        validators=[
            validators.MinLengthValidator(MIN_LEN_PHONE_NUMBER),
            validators.RegexValidator('08[789]\d{7}', 'The phone number you entered is invalid!')
        ]
    )

    town = models.CharField(
        blank=False,
        null=False,
        max_length=MAX_LEN_TOWN_NAME,
        validators=[validators.MinLengthValidator(MIN_LEN_TOWN_NAME)]
    )

    address = models.CharField(
        blank=False,
        null=False,
        max_length=MAX_LEN_ADDRESS,
        validators=[validators.MinLengthValidator(MIN_LEN_ADDRESS)]
    )

    post_code = models.CharField(
        blank=False,
        null=False,
        max_length=MAX_LEN_POST_CODE,
        validators=[
            validators.MinLengthValidator(MIN_LEN_POST_CODE),
            validators.integer_validator
        ]
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    # TODO: Make this when the order status is set to shipped to put on a shipping date
    shipping_date = models.DateField(
        blank=True,
        null=True
    )

    total_price = models.FloatField(
        default=0,
        blank=False,
        null=False
    )

    discount = models.ForeignKey(
        DiscountCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    discounted_price = models.FloatField(
        blank=True,
        null=True
    )

    order_status = models.CharField(
        choices=OrderStatusEnumMixin.choices(),
        max_length=OrderStatusEnumMixin.max_len(),
        default='InPreparation'
    )



class OrderItem(models.Model):
    MAX_DIGITS_PRICE = 10

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1,
        blank=False,
        null=False
    )

    price = models.FloatField(
        blank=False,
        null=False
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )


