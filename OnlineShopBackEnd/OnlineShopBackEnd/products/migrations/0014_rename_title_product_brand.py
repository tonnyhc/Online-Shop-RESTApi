# Generated by Django 3.2.16 on 2023-02-15 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='brand',
        ),
    ]
