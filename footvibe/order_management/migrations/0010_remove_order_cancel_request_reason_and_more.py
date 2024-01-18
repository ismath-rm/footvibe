# Generated by Django 4.2.7 on 2024-01-16 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order_management', '0009_order_cancel_request_reason_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancel_request_reason',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cancel_request_status',
        ),
        migrations.CreateModel(
            name='CancellationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]