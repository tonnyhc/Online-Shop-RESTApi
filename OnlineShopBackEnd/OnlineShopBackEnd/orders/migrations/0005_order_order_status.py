# Generated by Django 3.2.16 on 2023-03-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('InPreparation', 'In preparation'), ('Shipped', 'Shipped')], default='InPreparation', max_length=13),
            preserve_default=False,
        ),
    ]
