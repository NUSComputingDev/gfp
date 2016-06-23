# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-23 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
        ('scoreboard', '0002_auto_20160623_2226'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_on', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.Game')),
            ],
        ),
        migrations.CreateModel(
            name='RaffleTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Player')),
            ],
        ),
        migrations.AddField(
            model_name='draw',
            name='winning_ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.RaffleTicket', unique=True),
        ),
    ]
