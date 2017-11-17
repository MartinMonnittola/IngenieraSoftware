# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from game.models import *
from game.forms import *
from django.utils import timezone

class AllianceModelTestCase(TestCase):

    def setUp(self):
        user = User(username="Tester",
                    first_name="Tes",
                    last_name= "Ter",
                    email="tes@ter.com",
                    password="tester123")
        user.save()

        ally = User(username="Ally",
                       first_name="All",
                       last_name= "ied",
                       email="all@iance.com",
                       password="ally123")
        ally.save()
        
        game = Game.create(user, "TestGame", 4, 2)
        game.save()
        
        team1 = Alliance.create("Team 1", game)
        team1.save()
        
        origin = Planet.create(user, game, "TestLand", 1234, team1)
        origin.save()

        target = Planet.create(ally, game, "Friends4ever", 4321, team1)
        target.save()

    def test_associated_to_game(self):
        alliance = Alliance.objects.get(pk=1)
        game = Game.objects.get(pk=1)
        self.assertEqual(alliance.game, game)

    def test_has_name(self):
        alliance = Alliance.objects.get(pk=1)
        self.assertEqual(alliance.name, "Team 1")

    def test_starts_with_zero_players(self):
        alliance = Alliance.objects.get(pk=1)
        self.assertEqual(alliance.num_players, 0)

    def test_add_player(self):
        alliance = Alliance.objects.get(pk=1)
        alliance.add_player()
        self.assertEqual(alliance.num_players, 1)

    def test_remove_player(self):
        alliance = Alliance.objects.get(pk=1)
        alliance.add_player()
        self.assertEqual(alliance.num_players, 1)
        alliance.remove_player()
        self.assertEqual(alliance.num_players, 0)
    
    def test_send_population_target(self):
        alliance = Alliance.objects.get(pk=1)
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        old_population = target.population_qty
        origin.send_population(target)
        self.assertEqual(target.population_qty, (old_population + 100))

    def test_send_population_origin(self):
        alliance = Alliance.objects.get(pk=1)
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        old_population = origin.population_qty
        origin.send_population(target)
        self.assertEqual(origin.population_qty, (old_population - 100))
        
    def test_send_population_to_dead_planet(self):
        alliance = Alliance.objects.get(pk=1)
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        target.population_qty = 0
        target.save()
        error_msg = origin.send_population(target)
        self.assertEqual(error_msg, 0)
        
    def test_send_population_from_dyng_planet(self):
        alliance = Alliance.objects.get(pk=1)
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        origin.population_qty = 10
        origin.save()
        error_msg = origin.send_population(target)
        self.assertEqual(error_msg, 0)
