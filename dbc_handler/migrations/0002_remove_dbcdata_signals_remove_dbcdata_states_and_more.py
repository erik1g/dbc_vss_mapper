# Generated by Django 5.2.3 on 2025-07-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbc_handler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbcdata',
            name='signals',
        ),
        migrations.RemoveField(
            model_name='dbcdata',
            name='states',
        ),
        migrations.AddField(
            model_name='dbcdata',
            name='parsed_data',
            field=models.JSONField(default=dict),
        ),
    ]
