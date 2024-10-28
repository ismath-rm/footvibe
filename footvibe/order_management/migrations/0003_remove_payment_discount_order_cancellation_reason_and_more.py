# Generated by Django 5.0.6 on 2024-10-20 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0002_payment_order_payment"),
        ("product_management", "0007_auto_20231211_1310"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="discount",
        ),
        migrations.AddField(
            model_name="order",
            name="cancellation_reason",
            field=models.CharField(default="Damaged Product", max_length=150),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Pending ", "Pending"),
                    ("Accepted", "Accepted"),
                    ("Cancelled", "Cancelled"),
                    ("Delivered", "Delivered"),
                    ("Returned", "Returned"),
                    ("Requested for cancel", "Requested for cancel"),
                    ("Requested for return", "Requested for return"),
                ],
                default="New",
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name="OrderProduct",
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
                ("quantity", models.IntegerField(blank=True, default=0, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("ordered", models.BooleanField(default=False)),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order_management.order",
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order_management.payment",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product_management.product",
                    ),
                ),
                (
                    "product_variant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product_management.productvariant",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
