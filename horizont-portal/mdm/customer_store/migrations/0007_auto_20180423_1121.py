# Generated by Django 2.0.4 on 2018-04-23 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_store', '0006_auto_20180423_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerstoreimage',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
