# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-10 15:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0014_auto_20160606_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='display_leaderboard',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='guess',
            name='guessed_on',
            field=models.DateField(auto_now=True, default=datetime.datetime(2016, 6, 10, 15, 56, 24, 331854, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
