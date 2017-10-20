# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from .models import *
from .forms import *

class GameModelTestsCase(TestCase):

    def setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()
        game = Game.create(1, const_population=30, const_missil=30,
                           const_shield=40, 1, 1, 1, 1, user)
        game.save()
        planet = Planet.create(user, game, "LJBKHB")
        planet.save()

    """
    Metodos para realizar el testeo de la aplicacion.
    """
    def hurt_has_not_value_negative_or_zero(self):
        game = Room.objects.get(pk=1)
        self.assertGreater(game.hurt_to_shield, 0)
        self.assertGreater(game.hurt_to_poblation, 0)

    def const_has_not_value_negative_or_zero(self):
        game = Room.objects.get(pk=1)
        self.assertGreater(game.const_misil, 0)
        self.assertGreater(game.const_poblation, 0)
        self.assertGreater(game.const_shield, 0)

    def const_sum_is_not_value_greater_than_hundred(self):
        game = Room.objects.get(pk=1)
        self.assertLessEqual((game.const_misil + game.const_poblation +
                           game.const_shield), 100)

    def time_misil_has_not_value_negative_or_zero(self):
        self.assertGreater(game.time_misil, 0)

    def initial_poblation_has_not_value_negative_or_zero(self):
        self.assertGreater(game.initial_poblation, 0)

    def can_deactivate_a_planet(self):
        planet = Planet.objects.get(pk=1)
        game = Room.objects.get(pk=1)
        self.assertTrue(game.deactivatePlanet(planet.id))

    def can_start_game(self):
        game = Room.objects.get(pk=1)
        game.startGame()
        self.assertTrue(game.game_started)

    def can_join_game(self):
        game = Room.objects.get(pk=1)
        user = User(username="JJJ", first_name="JJJLJH", last_name= "JJJLKGLVJ",
                    email="dv@gmail.com", password="Aa12345678")
        user.save()
        game.joinGame(user.id, "Sion")
        self.assertTrue(game.joinGame(user.id, "Sion"))

    def can_create_game():
        game = Room.createGame(1, 30, 30, 40, 1, 1, 1, 1, user)
        game.save()

class CreateGameTestsCase(TestCase):
    def setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()

    def form_field_hurt_poblation_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)

    def form_field_hurt_shield_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {
            "room_name": "DEFAULT",
            "init_population": 1,
            "const_missile":30,
            "const_shield":30,
            "const_poblation":40,
            "missile_delay":1,
            "population_damage_per_missile":1,
            "shield_damage_per_missile":1,
            "max_players":20,
            "creator":user
        }
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)

    def form_field_const_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)

    def const_sum_is_not_value_greater_than_hundred(self):
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)
        self.assertLessEqual((form_data["const_misil"] +
                              form_data["const_poblation"] +
                              form_data["const_shield"]), 100)

    def form_field_time_misil_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)

    def form_field_initial_poblation_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid)
