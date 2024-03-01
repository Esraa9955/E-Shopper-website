# Generated by Django 4.2.10 on 2024-03-01 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0006_rename_thumbnail_product_image_remove_product_images_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="product/multiImages/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="thumbnail",
            field=models.ImageField(
                default="static/images/notfound.png", upload_to="product/images/"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True, related_name="products", to="product.productimage"
            ),
        ),
    ]
