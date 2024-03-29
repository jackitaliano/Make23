# Generated by Django 4.1.7 on 2023-03-13 03:41

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_id', models.CharField(default=api.models.generate_unique_code, max_length=16, unique=True)),
                ('transcript', models.TextField(default='', null=True)),
                ('notes', models.TextField(default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
