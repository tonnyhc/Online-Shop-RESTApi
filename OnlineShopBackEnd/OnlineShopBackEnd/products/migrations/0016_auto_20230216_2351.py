# Generated by Django 3.2.16 on 2023-02-16 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]