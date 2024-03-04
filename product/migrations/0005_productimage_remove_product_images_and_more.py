# Generated by Django 4.2.10 on 2024-03-01 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_remove_product_images_alter_product_thumbnail_and_more"),
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
        migrations.RemoveField(model_name="product", name="images",),
        migrations.AlterField(
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