# Generated by Django 2.0.4 on 2018-05-05 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0004_auto_20180505_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routecustomerstore',
            name='status',
            field=models.CharField(choices=[('CHECKIN', 'Check-in'), ('SURVEY', 'Survey'), ('PREORDER', 'PreOrder'), ('PAYMENT', 'Payment')], default=None, max_length=10, null=True),
        ),
    ]