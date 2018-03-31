# Generated by Django 2.0.2 on 2018-03-31 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandize', '0004_auto_20180331_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='merchandize.Category'),
        ),
        migrations.AlterUniqueTogether(
            name='merchandize',
            unique_together={('barcode', 'itemcode')},
        ),
    ]