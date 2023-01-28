from django.contrib.auth import get_user_model
from django.db import models

from OnlineShopBackEnd.products.models import Product

UserModel = get_user_model()

#TODO: Finish the order model
class Order(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT
    )
    order_date = models.DateField(
        auto_now_add=True,
    )


