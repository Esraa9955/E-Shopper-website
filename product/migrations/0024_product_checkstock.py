# Generated by Django 5.0.3 on 2024-03-23 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_product_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='checkstock',
            field=models.IntegerField(default=0),
        ),
    ]
