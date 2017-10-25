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
        
        game = Game.create(user, "TestGame", 4)
        game.save()
        
        origin = Planet.create(user, game, "TestLand", 1234)
        origin.save()
        target = Planet.create(oponent, game, "GonnaLose", 4321)
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
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        missile = Missile.objects.get(pk=1)
        missile.deal_damage()
        self.assertLess(target.shield_perc, 100)
    
    def test_damage_dealt_on_pop(self):
        origin = Planet.objects.get(pk=1)
        target = Planet.objects.get(pk=2)
        missile = Missile.objects.get(pk=1)
        missile.deal_damage()
        self.assertLess(target.population_qty, 5000)
