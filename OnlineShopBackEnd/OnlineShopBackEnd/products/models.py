from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.text import slugify

from cloudinary.models import CloudinaryField

from OnlineShopBackEnd.products.mixins import CategoryEnumMixin, GenderEnumMixin

UserModel = get_user_model()


class ProductRating(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    score = models.FloatField(
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(5),
        ],
    )


class Category(models.Model):
    category = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.category


# TODO: must add a quantity
class Product(models.Model):
    MAX_LEN_TITLE = 155
    MAX_LEN_PRODUCT_ID = 25
    MAX_LEN_MODEL = 155

    brand = models.CharField(
        max_length=MAX_LEN_TITLE,
        null=False,
        blank=False,
    )

    model = models.CharField(
        max_length=MAX_LEN_MODEL,
        null=False,
        blank=False
    )

    product_price = models.FloatField(
        null=False,
        blank=False,
    )
    discounted_price = models.FloatField(
        null=True,
        blank=True
    )
    product_id = models.CharField(
        max_length=MAX_LEN_PRODUCT_ID,
        unique=True,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        blank=True,
    )
    quantity = models.PositiveIntegerField(
        default=0,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,

    )
    ratings = models.ManyToManyField(
        ProductRating,
        related_name='products',
    )

    gender = models.CharField(
        choices=GenderEnumMixin.choices(),
        max_length=GenderEnumMixin.max_len()
    )

    is_published = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )

    # This 2 are for the slug field. The first one generates the slug out of title and product_id
    # The save method just saves the model with the populated slug_field
    def generate_slug(self):
        return slugify(f"{self.brand}-{self.product_id}")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.brand + ' ' + self.model


class FavoriteProducts(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    image = CloudinaryField('image')
