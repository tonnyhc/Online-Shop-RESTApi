# Generated by Django 3.2.16 on 2023-01-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_sunglasses_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sunglasses',
            name='category',
            field=models.CharField(choices=[('Sunglasses', 'Sunglasses'), ('Prism', 'Prism'), ('Lens', 'Lens'), ('Cases', 'Cases')], default='Sunglasses', max_length=10),
            preserve_default=False,
        ),
    ]
