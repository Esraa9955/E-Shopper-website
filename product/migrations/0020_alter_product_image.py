# Generated by Django 5.0.2 on 2024-03-10 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_remove_product_sizeable_remove_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product/images/'),
        ),
    ]
