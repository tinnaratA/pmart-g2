# Generated by Django 2.0.4 on 2018-05-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0006_auto_20180505_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='routecustomerstore',
            name='comment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
