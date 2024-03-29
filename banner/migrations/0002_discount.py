# Generated by Django 5.0.2 on 2024-03-15 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(default='static/images/notfound.png', upload_to='discounts/images')),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('sale_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('end_date', models.DateTimeField()),
            ],
        ),
    ]
