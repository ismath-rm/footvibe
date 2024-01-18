# Generated by Django 4.2.7 on 2024-01-06 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0004_remove_orderproduct_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], default='New', max_length=10),
        ),
    ]
