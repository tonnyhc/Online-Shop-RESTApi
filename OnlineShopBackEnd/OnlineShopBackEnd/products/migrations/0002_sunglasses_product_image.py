# Generated by Django 3.2.16 on 2023-01-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sunglasses',
            name='product_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
