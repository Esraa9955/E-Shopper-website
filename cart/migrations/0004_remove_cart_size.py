# Generated by Django 5.0.2 on 2024-03-12 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cart_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='size',
        ),
    ]