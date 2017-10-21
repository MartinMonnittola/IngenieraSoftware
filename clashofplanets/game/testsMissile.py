# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from game.models import *
from game.forms import *
from django.utils import timezone

class MissileModelTestCase(TestCase):

    def setup(self):
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
        
        game = Room.createGame(1, 30, 30, 40, 1, 1, 1, 1, user)
        game.save()
        
        origin = Planet.create(user, game, "TestLand", 1234)
        origin.save()
        target = Planet.create(oponent, game, "Gonnalose", 4321)
        target.save()
        
        missile = Missile(user, oponent)
        missile.save()
    
    def test_missile_has_target(self):
        user = User.objects(username = "Tester")
        oponent = User.objects.get(username = "Oponent")
        missile = Missile.objects.get(owner = user)
        self.assertEqual(missile.target, oponent)

    def test_missile_has_owner(self):
        user = User.objects.get(pk=2)
        oponent = User.objects.get(username = "Oponent")
        missile = Missile.objects.get(target = oponent)
        self.assertEqual(missile.owner, user)

