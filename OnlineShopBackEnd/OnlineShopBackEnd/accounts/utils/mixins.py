from enum import Enum

from OnlineShopBackEnd.products.mixins import ChoicesEnumMixin


class Gender(ChoicesEnumMixin, Enum):
    Man = 'Man'
    Woman = "Woman"
    DoNotShow = 'Do not show'

