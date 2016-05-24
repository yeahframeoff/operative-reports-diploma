# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-23 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remote_db', '0002_widgetconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagram_type', models.CharField(choices=[('R', 'Round'), ('S', 'Stacked'), ('C', 'Curve')], max_length=1)),
                ('query', models.TextField()),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_db.Dashboard')),
            ],
        ),
        migrations.RemoveField(
            model_name='widgetconfig',
            name='owner',
        ),
        migrations.DeleteModel(
            name='WidgetConfig',
        ),
    ]
