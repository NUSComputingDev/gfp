# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-29 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0005_auto_20160430_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='position',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
