# Generated by Django 2.0.2 on 2018-04-08 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_extension', '0002_auto_20180408_0146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoriteproduct',
            old_name='variant',
            new_name='variants',
        ),
    ]
