# Generated by Django 2.0.4 on 2018-04-22 20:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('line1', models.TextField()),
                ('line2', models.TextField()),
                ('district', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('province', models.CharField(max_length=256)),
                ('postcode', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'address',
                'permissions': (('view_address', 'Can view common addresses'),),
            },
        ),
        migrations.CreateModel(
            name='HumanName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('first', models.CharField(max_length=512)),
                ('middle', models.CharField(max_length=512)),
                ('last', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'human_name',
                'permissions': (('view_name', 'Can view human names'),),
            },
        ),
    ]