from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.text import slugify

from OnlineShopBackEnd.products.mixins import CategoryEnumMixin

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


class Product(models.Model):
    MAX_LEN_TITLE = 155
    MAX_LEN_PRODUCT_ID = 25
    MAX_LEN_MODEL = 155

    title = models.CharField(
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
    category = models.CharField(
        choices=CategoryEnumMixin.choices(),
        max_length=CategoryEnumMixin.max_len(),
    )
    ratings = models.ManyToManyField(
        ProductRating,
        related_name='products',
        blank=True,
        null=True,
    )

    #This 2 are for the slug field. The first one generates the slug out of title and product_id
    #The save method just saves the model with the populated slug_field
    def generate_slug(self):
        return slugify(f"{self.title}-{self.product_id}")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title + ' ' + self.product_id

#This model is for the images for the products, because i want to have more than 1 image for a single product
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    #TODO: make the image field and ImageField and upload it to some cloud
    image = models.URLField()