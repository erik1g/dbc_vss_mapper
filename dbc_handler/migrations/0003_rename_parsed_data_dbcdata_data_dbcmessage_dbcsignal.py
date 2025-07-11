# Generated by Django 5.2.3 on 2025-07-07 13:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbc_handler', '0002_remove_dbcdata_signals_remove_dbcdata_states_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dbcdata',
            old_name='parsed_data',
            new_name='data',
        ),
        migrations.CreateModel(
            name='DBCMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('frame_id', models.CharField(blank=True, max_length=64, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('senders', models.JSONField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, null=True)),
                ('dbc_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='dbc_handler.dbcdata')),
            ],
        ),
        migrations.CreateModel(
            name='DBCSignal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('unit', models.CharField(blank=True, max_length=64, null=True)),
                ('start_bit', models.IntegerField(blank=True, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('byte_order', models.CharField(blank=True, max_length=32, null=True)),
                ('is_signed', models.BooleanField(default=False)),
                ('scale', models.FloatField(blank=True, null=True)),
                ('offset', models.FloatField(blank=True, null=True)),
                ('minimum', models.FloatField(blank=True, null=True)),
                ('maximum', models.FloatField(blank=True, null=True)),
                ('choices', models.JSONField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, null=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signals', to='dbc_handler.dbcdata')),
            ],
        ),
    ]
