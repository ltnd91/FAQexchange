# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-28 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20180428_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
