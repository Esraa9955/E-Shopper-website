# Generated by Django 5.0.2 on 2024-03-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_category_imageurl_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='imageUrl',
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='static/images/notfound.png', upload_to='category/images'),
        ),
    ]
