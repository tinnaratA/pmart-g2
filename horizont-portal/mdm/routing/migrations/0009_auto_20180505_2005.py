# Generated by Django 2.0.4 on 2018-05-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0008_auto_20180505_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routecustomerstore',
            name='status',
            field=models.CharField(choices=[('CHECKIN', 'Check-in'), ('SURVEY', 'Survey'), ('PREORDER', 'PreOrder'), ('PAYMENT', 'Payment')], default='SURVEY', max_length=10, null=True),
        ),
    ]
