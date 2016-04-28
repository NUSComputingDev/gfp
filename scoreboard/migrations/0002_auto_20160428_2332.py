# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 15:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scoreboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ['-score']},
        ),
        migrations.AddField(
            model_name='score',
            name='game_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.GameSession'),
            preserve_default=False,
        ),
    ]
