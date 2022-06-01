# Generated by Django 4.0.4 on 2022-06-01 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feeds',
            old_name='field1',
            new_name='LWS',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='field2',
            new_name='battery_status',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='field3',
            new_name='humidity',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='c_id',
            new_name='node_id',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='field4',
            new_name='soil_moisture',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='field5',
            new_name='soil_temprature',
        ),
        migrations.RenameField(
            model_name='feeds',
            old_name='field6',
            new_name='temprature',
        ),
        migrations.RemoveField(
            model_name='feeds',
            name='entry_id',
        ),
        migrations.RemoveField(
            model_name='feeds',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='feeds',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]