# Generated by Django 4.2.7 on 2024-01-17 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0012_remove_cancellationrequest_admin_comments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancellation_requested',
        ),
        migrations.DeleteModel(
            name='CancellationRequest',
        ),
    ]
