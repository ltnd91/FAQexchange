# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-28 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_auto_20180428_2017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='message',
            new_name='name',
        ),
    ]
