# Generated by Django 3.2.16 on 2023-01-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_sunglasses_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155)),
                ('product_price', models.FloatField()),
                ('product_id', models.IntegerField()),
                ('product_image', models.URLField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Sunglasses', 'Sunglasses'), ('Prism', 'Prism'), ('Lens', 'Lens'), ('Cases', 'Cases')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Sunglasses',
        ),
    ]
