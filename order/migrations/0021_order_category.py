# Generated by Django 5.0.3 on 2024-03-26 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_remove_category_itemcount'),
        ('order', '0020_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
        ),
    ]
