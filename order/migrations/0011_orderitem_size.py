# Generated by Django 5.0.2 on 2024-03-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_ordertmp_alter_orderitem_product_orderitemtmp'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='', max_length=200),
        ),
    ]