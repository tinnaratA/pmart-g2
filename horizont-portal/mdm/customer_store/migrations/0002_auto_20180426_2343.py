# Generated by Django 2.0.4 on 2018-04-26 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerStoreGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('A', 'Grade A'), ('B', 'Grade B'), ('C', 'Grade C'), ('D', 'Grade D')], default='D', max_length=10)),
                ('higher_grade', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='higher', to='customer_store.CustomerStoreGrade')),
                ('lower_grade', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='lower', to='customer_store.CustomerStoreGrade')),
            ],
            options={
                'db_table': 'customer_store_grade',
            },
        ),
        migrations.AddField(
            model_name='customerstore',
            name='grade',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='customer_store.CustomerStoreGrade'),
        ),
    ]
