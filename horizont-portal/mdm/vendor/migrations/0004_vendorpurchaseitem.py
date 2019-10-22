# Generated by Django 2.0.4 on 2018-05-16 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_auto_20180516_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPurchaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_purchase_items', to='vendor.PurchaseItem')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_purchase_items', to='vendor.Vendor')),
            ],
            options={
                'db_table': 'vendor_purchase_item',
            },
        ),
    ]