# Generated by Django 5.0.2 on 2024-03-26 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_remove_order_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='isReady',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'pending'), ('S', 'shipped'), ('D', 'delivered'), ('C', 'cancelled'), ('R', 'ready'), ('F', 'failed'), ('M', 'paid')], default='P', max_length=50),
        ),
    ]