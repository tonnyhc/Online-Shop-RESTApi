from django.db import models

from OnlineShopBackEnd.products.mixins import CategoryEnumMixin

class Product(models.Model):
    MAX_LEN_TITLE = 155
    MAX_LEN_PRODUCT_ID = 25

    title = models.CharField(
        max_length=MAX_LEN_TITLE,
        null=False,
        blank=False,
    )

    product_price = models.FloatField(
        null=False,
        blank=False,
    )
    product_id = models.CharField(
        max_length=MAX_LEN_PRODUCT_ID,
        unique=True,
        null=False,
        blank=False,
    )
    product_image = models.URLField(
        blank=True,
        null=True,
    )

    category = models.CharField(
        choices=CategoryEnumMixin.choices(),
        max_length=CategoryEnumMixin.max_len(),
    )
