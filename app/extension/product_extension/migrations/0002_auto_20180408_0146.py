# Generated by Django 2.0.2 on 2018-04-08 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_extension', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriteproduct',
            name='customer',
        ),
        migrations.AddField(
            model_name='favoriteproduct',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
