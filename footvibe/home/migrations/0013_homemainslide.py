# Generated by Django 4.2.7 on 2024-01-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_wallet_wallethistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeMainSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=20)),
                ('subheading', models.CharField(max_length=30, null=True)),
                ('slide_image', models.ImageField(upload_to='banners')),
            ],
        ),
    ]
