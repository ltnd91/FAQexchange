# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-28 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_auto_20180428_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='name',
            field=models.TextField(blank=True),
        ),
    ]
