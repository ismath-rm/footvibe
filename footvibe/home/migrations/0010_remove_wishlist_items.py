# Generated by Django 4.2.7 on 2024-01-09 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_wishlist_options_alter_wishlistitems_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='items',
        ),
    ]
