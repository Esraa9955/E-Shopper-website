# Generated by Django 5.0.2 on 2024-02-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_ssn_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_password',
            field=models.CharField(default='', max_length=255),
        ),
    ]
