# Generated by Django 3.2.16 on 2023-03-12 13:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_appuser_birth_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='full_name',
            field=models.CharField(default='Toni Petro', max_length=50, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.RegexValidator(message='Please enter a valid full name!', regex="/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u")]),
            preserve_default=False,
        ),
    ]
