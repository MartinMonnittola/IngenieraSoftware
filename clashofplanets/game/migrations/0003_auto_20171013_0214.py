# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20171012_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamebot',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='gamebot',
            name='game',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='planet',
            name='game',
        ),
        migrations.RemoveField(
            model_name='planet',
            name='player',
        ),
        migrations.AddField(
            model_name='partida',
            name='max_players',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='partida',
            name='playing',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partida',
            name='const_misil',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='const_poblation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='const_shield',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='hurt_to_poblation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='hurt_to_shield',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='initial_poblation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partida',
            name='time_misil',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Bot',
        ),
        migrations.DeleteModel(
            name='GameBot',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.DeleteModel(
            name='Planet',
        ),
    ]