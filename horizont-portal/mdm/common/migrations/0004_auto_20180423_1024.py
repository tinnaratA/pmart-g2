# Generated by Django 2.0.4 on 2018-04-23 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20180423_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='line2',
            field=models.TextField(blank=True),
        ),
    ]
