# Generated by Django 2.0.4 on 2018-04-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='sku',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
