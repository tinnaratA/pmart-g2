# Generated by Django 2.0.4 on 2018-05-17 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180429_0110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saledeliverydetail',
            old_name='company_address',
            new_name='address',
        ),
    ]
