# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-05 08:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0011_auto_20160605_1548'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='partialscore',
            unique_together=set([('aggregated_score', 'game_master')]),
        ),
    ]
