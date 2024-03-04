# Generated by Django 5.0.2 on 2024-03-03 15:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3), django.core.validators.MaxLengthValidator(limit_value=30)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3), django.core.validators.MaxLengthValidator(limit_value=30)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='shopname',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]