# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    Game,
    list_display=[
        "id", "game_name", "user", "connected_players", "num_alliances", "max_players", "bot_players",
        "game_started", "initial_population", "const_population",
        "const_shield", "const_missile", "hurt_to_population",
        "hurt_to_shield"],
    list_display_links=["id", "game_name"],
)
admin.site.register(
    Planet,
    list_display=[
        "id", "name", "player", "game",
        "seed", "alliance", "population_qty", "shield_perc", "missiles_qty",
        "population_distr", "shield_distr", "missile_distr",
    ],
    list_display_links=["id", "name",],
)
admin.site.register(
    Alliance,
    list_display=["id", "name", "game"],
    list_display_links=["id", "name",],
)
