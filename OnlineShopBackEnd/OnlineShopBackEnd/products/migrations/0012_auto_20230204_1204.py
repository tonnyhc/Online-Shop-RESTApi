# Generated by Django 3.2.16 on 2023-02-04 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
        migrations.AlterField(
            model_name='product',
            name='ratings',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='products.ProductRating'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
    ]