# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 14:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remote_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WidgetConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagram_type', models.CharField(choices=[('R', 'Round'), ('S', 'Stacked'), ('C', 'Curve')], max_length=1)),
                ('query', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
