# Generated by Django 2.0.4 on 2018-05-17 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0009_auto_20180505_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='stores',
        ),
    ]
