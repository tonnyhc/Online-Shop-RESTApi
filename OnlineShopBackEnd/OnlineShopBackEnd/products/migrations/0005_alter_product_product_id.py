# Generated by Django 3.2.16 on 2023-01-29 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20230128_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
