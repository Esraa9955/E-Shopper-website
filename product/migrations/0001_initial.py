# Generated by Django 5.0.2 on 2024-02-28 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(default='static/images/notfound.png', upload_to='product/images/')),
                ('description', models.TextField(default='', max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('add_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('brand', models.CharField(default='', max_length=225)),
                ('stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
