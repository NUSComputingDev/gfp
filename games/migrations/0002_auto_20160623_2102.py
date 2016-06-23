# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-23 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
        ('games', '0001_initial'),
        ('scoreboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guess',
            name='game_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.GameSession'),
        ),
        migrations.AddField(
            model_name='guess',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Player'),
        ),
    ]