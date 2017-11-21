# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from game.models import *
from game.forms import *
from django.utils import timezone

class PlanetModelTestCase(TestCase):

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

        planet = Planet.create(user, game, "TestLand", 1234, team1)
        planet.save()

        target = Planet.create(oponent, game, "GonnaLose", 4321, team2)
        target.save()

    def test_planet_has_owner(self):
        user = User.objects.get(pk=1)
        planet = Planet.objects.get(pk=1)
        self.assertEqual(planet.player.username, user.username)

    def test_planet_population_assignment(self):
        planet = Planet.objects.get(pk=1)
        planet.assign_perc_rate(100,0,0)
        self.assertEqual(planet.population_distr, 100)

    def test_planet_shield_assignment(self):
        planet = Planet.objects.get(pk=1)
        planet.assign_perc_rate(0,100,0)
        self.assertEqual(planet.shield_distr, 100)

    def test_planet_missile_assignment(self):
        planet = Planet.objects.get(pk=1)
        planet.assign_perc_rate(0,0,100)
        self.assertEqual(planet.missile_distr, 100)

    def test_planet_cant_assign_greater_than_100(self):
        planet = Planet.objects.get(pk=1)
        with self.assertRaises(NameError, msg='Wrong Distribution Choice'):
            planet.assign_perc_rate(75,75,75)

    def test_planet_cant_assign_less_than_100(self):
        planet = Planet.objects.get(pk=1)
        with self.assertRaises(NameError, msg='Wrong Distribution Choice'):
            planet.assign_perc_rate(25,25,25)

    def test_planet_decrease_shield(self):
        planet = Planet.objects.get(pk=1)
        planet.decrease_shield(25)
        self.assertEqual(planet.shield_perc, 75)

    def test_planet_decrease_population(self):
        planet = Planet.objects.get(pk=1)
        planet.decrease_population(25)
        correct_qty = planet.game.initial_population - 25
        self.assertEqual(planet.population_qty, correct_qty)

    def test_planet_doesnt_have_missiles(self):
        planet = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        success = planet.launch_missile(target)
        self.assertEqual(success, False)

    def test_planet_can_launch_missiles(self):
        planet = Planet.objects.get(pk=1)
        planet.missiles_qty = 1
        target = Planet.objects.get(pk=2)
        success = planet.launch_missile(target)
        self.assertEqual(success, True)

    def test_planet_missile_state(self):
        planet = Planet.objects.get(pk=1)
        planet.missiles_qty = 1
        target = Planet.objects.get(pk=2)
        success = planet.launch_missile(target)
        times = planet.get_missiles_state()
        self.assertGreaterEqual(times["GonnaLose"], timezone.timedelta(seconds=0))
