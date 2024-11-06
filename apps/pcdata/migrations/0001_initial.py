# Generated by Django 5.1.2 on 2024-11-01 20:35

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='pcinfo',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField(null=True)),
                ('os', models.TextField(max_length=140, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='pcdata',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('cpu_json', models.JSONField(blank=True, null=True)),
                ('gpu_json', models.JSONField(blank=True, null=True)),
                ('memory_json', models.JSONField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('pc', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pcdata.pcinfo')),
            ],
        ),
    ]