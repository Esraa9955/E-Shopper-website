# Generated by Django 5.0.2 on 2024-03-05 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
