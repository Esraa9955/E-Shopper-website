# Generated by Django 5.0.2 on 2024-03-05 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_rename_buyer_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
