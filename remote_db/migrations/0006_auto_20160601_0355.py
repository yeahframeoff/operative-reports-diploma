# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_db', '0005_widget_db_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='columns',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='widget',
            name='query',
            field=models.TextField(null=True),
        ),
    ]
