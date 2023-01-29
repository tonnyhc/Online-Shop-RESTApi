from django.contrib import admin
from django.contrib.auth import get_user_model

from OnlineShopBackEnd.accounts.models import UserInfo

UserModel = get_user_model()

@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass

