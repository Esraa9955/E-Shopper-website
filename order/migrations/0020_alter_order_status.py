# Generated by Django 5.0.2 on 2024-03-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_orderitem_isready_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'pending'), ('S', 'shipped'), ('D', 'delivered'), ('C', 'cancelled'), ('R', 'ready'), ('F', 'failed'), ('RF', 'refunded')], default='P', max_length=50),
        ),
    ]
