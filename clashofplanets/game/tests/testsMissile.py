# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from game.models import *
from game.forms import *
from django.utils import timezone

class MissileModelTestCase(TestCase):

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

        game = Game.create(user, "TestGame", 4, 2, 1)
        game.save()

        team1 = Alliance.create("Team 1", game)
        team1.save()

        team2 = Alliance.create("Team 2", game)
        team2.save()

        origin = Planet.create(user, game, "TestLand", 1234, team1)
        origin.save()
        target = Planet.create(oponent, game, "GonnaLose", 4321, team2)
        target.save()

        missile = Missile.create(origin, target)
        missile.save()

    def test_missile_has_target(self):
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        missile = Missile.objects.get(owner = origin)
        self.assertEqual(missile.target, target)

    def test_missile_has_owner(self):
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        missile = Missile.objects.get(target = target)
        self.assertEqual(missile.owner, origin)

    def test_damage_dealt_on_shield(self):
        missile = Missile.objects.get(pk=1)
        missile.deal_damage()
        self.assertLess(Planet.objects.get(pk=2).shield_perc, 100)

    def test_damage_dealt_on_pop(self):
        target = Planet.objects.get(pk=2)
        target.decrease_shield(100)
        target.save()
        missile = Missile.objects.get(pk=1)
        missile.deal_damage()
        planet = Planet.objects.get(pk=2)
        self.assertLess(planet.population_qty,
                        planet.game.initial_population)

    def test_time_to_target_returns_right_value(self):
        missile = Missile.objects.get(pk=1)
        time = missile.time_to_target()
        self.assertLess(time, timezone.timedelta(seconds=missile.owner.game.time_missile))
