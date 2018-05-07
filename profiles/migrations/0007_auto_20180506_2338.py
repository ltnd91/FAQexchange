# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-06 23:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20180425_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='activation_key',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='is_following_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='viewers',
            field=models.ManyToManyField(blank=True, related_name='is_viewing_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]