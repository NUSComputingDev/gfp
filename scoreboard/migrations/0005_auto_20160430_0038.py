# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-29 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0004_auto_20160429_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ['position']},
        ),
        migrations.RemoveField(
            model_name='score',
            name='score',
        ),
        migrations.AddField(
            model_name='score',
            name='position',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='scoreboard.GamePrize'),
            preserve_default=False,
        ),
    ]