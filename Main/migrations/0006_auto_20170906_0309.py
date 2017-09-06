# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_record_day_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='end_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='start_time',
            field=models.IntegerField(null=True),
        ),
    ]
