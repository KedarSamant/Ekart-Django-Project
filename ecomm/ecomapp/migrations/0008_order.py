# Generated by Django 5.1.7 on 2025-03-17 17:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ecomapp", "0007_remove_category_qty_cart_qty"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("order_id", models.CharField(max_length=100)),
                ("qty", models.IntegerField(default=1)),
                (
                    "pid",
                    models.ForeignKey(
                        db_column="pid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ecomapp.product",
                    ),
                ),
                (
                    "uid",
                    models.ForeignKey(
                        db_column="uid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
