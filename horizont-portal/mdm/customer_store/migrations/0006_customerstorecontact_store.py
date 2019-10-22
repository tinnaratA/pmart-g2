# Generated by Django 2.0.4 on 2018-05-05 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_store', '0005_auto_20180501_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerstorecontact',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_store_contacts', to='customer_store.CustomerStore'),
            preserve_default=False,
        ),
    ]