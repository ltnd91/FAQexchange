# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-24 00:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0002_topic_checked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='checked',
        ),
        migrations.AddField(
            model_name='topic',
            name='display',
            field=models.ManyToManyField(blank=True, related_name='is_displayT', to=settings.AUTH_USER_MODEL),
        ),
    ]
