# Generated by Django 5.0.2 on 2024-03-15 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_remove_category_imageurl_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='itemCount',
        ),
    ]
