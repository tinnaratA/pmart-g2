# Generated by Django 2.0.4 on 2018-05-05 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0002_routetaskorder_routetaskquestionaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='routeactivitytask',
            name='status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
