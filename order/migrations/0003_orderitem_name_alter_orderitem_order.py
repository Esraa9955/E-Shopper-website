# Generated by Django 5.0.2 on 2024-02-29 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_city_order_country_order_state_order_street_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='order.order'),
        ),
    ]
