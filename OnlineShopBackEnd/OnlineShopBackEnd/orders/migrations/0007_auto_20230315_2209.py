# Generated by Django 3.2.16 on 2023-03-15 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('InPreparation', 'In preparation'), ('Shipped', 'Shipped')], default='InPreparation', max_length=13),
        ),
    ]
