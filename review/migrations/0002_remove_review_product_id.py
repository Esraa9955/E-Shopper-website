# Generated by Django 5.0.2 on 2024-02-27 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='product_id',
        ),
    ]
