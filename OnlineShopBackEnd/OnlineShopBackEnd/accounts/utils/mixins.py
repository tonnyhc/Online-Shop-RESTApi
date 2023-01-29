from enum import Enum

from OnlineShopBackEnd.products.mixins import ChoicesEnumMixin


class Gender(ChoicesEnumMixin, Enum):
    Male = 'Male'
    Female = "Female"
    DoNotShow = 'Do not show'

