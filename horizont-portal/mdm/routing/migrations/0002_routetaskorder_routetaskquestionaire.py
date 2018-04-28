# Generated by Django 2.0.4 on 2018-04-28 18:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('questionaire', '0001_initial'),
        ('routing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteTaskOrder',
            fields=[
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_orders', to='routing.RouteActivityTask')),
            ],
            options={
                'db_table': 'route_task_order',
            },
        ),
        migrations.CreateModel(
            name='RouteTaskQuestionaire',
            fields=[
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='task_questionaire', to='routing.RouteActivityTask')),
                ('questions', models.ManyToManyField(to='questionaire.QuestionaireTemplate')),
            ],
            options={
                'db_table': 'route_task_questionaire',
            },
        ),
    ]
