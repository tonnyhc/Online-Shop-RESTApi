from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.datetime_safe import datetime

from OnlineShopBackEnd.accounts.utils.mixins import Gender


class AppUser(AbstractBaseUser, PermissionsMixin):
    MAX_LEN_USERNAME = 50
    MIN_LEN_USERNAME = 3
    MAX_LEN_FULL_NAME = 50
    MIN_LEN_FULL_NAME = 3

    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        unique=True,
        max_length=MAX_LEN_USERNAME,
        help_text=("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator, validators.MinLengthValidator(MIN_LEN_USERNAME)],
        error_messages={
            "unique": "A user with that username already exists.",
        }
    )
    full_name = models.CharField(
        max_length=MAX_LEN_FULL_NAME,
        validators=[validators.MinLengthValidator(MIN_LEN_FULL_NAME),
                    validators.RegexValidator(regex=r'^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.\'-]+$',
                                              message="Please enter a valid full name!")]
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with that email address already exists."
        }
    )
    gender = models.CharField(
        blank=True,
        null=True,
        choices=Gender.choices(),
        max_length=Gender.max_len(),
    )

    birth_year = models.DateField()

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)
    last_login = models.DateTimeField(
        ('last login'),
        default=datetime.now
    )
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.username

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserInfo(models.Model):
    MAX_LEN_BIO = 50
    MAX_LEN_FULLNAME = 110
    MAX_LEN_ADDRESS = 200
    MAX_LEN_CITY = 100
    MAX_LEN_PHONE_NUMBER = 20
    # relation with the user model
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE
    )
    # user names
    full_name = models.CharField(
        max_length=MAX_LEN_FULLNAME,
        blank=True,
        null=True,
    )

    # address info
    city = models.CharField(
        max_length=MAX_LEN_CITY,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=MAX_LEN_ADDRESS,
        blank=True,
        null=True,
    )
    post_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=MAX_LEN_PHONE_NUMBER,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "user info"
        verbose_name_plural = 'users info'

    @receiver(post_save, sender=AppUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserInfo.objects.create(user=instance)

    @receiver(post_save, sender=AppUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userinfo.save()

    def __str__(self):
        username = str(AppUser.objects.filter(pk=self.user_id).get())
        return username
