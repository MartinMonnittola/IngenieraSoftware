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

        oponent = User(username="Oponent",
                       first_name="Arch",
                       last_name= "Enemy",
                       email="arch@enemy.com",
                       password="oponent123")
        oponent.save()
        
        game = Game.create(user, "TestGame", 4)
        game.save()
        
        team1 = Alliance.create("Team 1", game)
        team1.save()

        team2 = Alliance.create("Team 2", game)
        team2.save()
        
        origin = Planet.create(user, game, "TestLand", 1234, team1)
        origin.save()

        target = Planet.create(oponent, game, "GonnaLose", 4321, team2)
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