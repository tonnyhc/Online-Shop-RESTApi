# Generated by Django 3.2.16 on 2023-03-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('InPreparation', 'In preparation'), ('Shipped', 'Shipped')], default='In preparation', max_length=13),
        ),
    ]
