# Generated by Django 5.0.2 on 2024-03-01 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ratings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
