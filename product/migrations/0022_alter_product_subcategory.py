# Generated by Django 5.0.2 on 2024-03-10 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_subcategory'),
        ('product', '0021_product_sizeable_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.subcategory'),
        ),
    ]
