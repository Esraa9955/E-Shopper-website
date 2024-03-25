# Generated by Django 5.0.3 on 2024-03-25 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'pending'), ('S', 'shipped'), ('D', 'delivered'), ('C', 'Cancelled')], default='P', max_length=50),
        ),
    ]