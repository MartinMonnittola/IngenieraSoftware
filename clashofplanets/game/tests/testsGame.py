from django.test import TestCase

# Create your tests here.
from game.models import *
from game.forms import *

class GameModelTestsCase(TestCase):

    def setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()

        game = Game.create(name="GuerraPlanetaria", max_players=20, owner=user, num_alliances=2)
        game.save()

        team1 = Alliance.create("Team 1", game)
        team1.save()

        planet = Planet.create(player=user, game=game, name="Tierra",seed =1, alliance=team1)
        planet.save()

    """
    Metodos para realizar el testeo de la aplicacion.
    """
    def test_hurt_shield_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.hurt_to_shield, 0)

    def test_hurt_population_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.hurt_to_population, 0)

    def test_const_missil_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.const_missile, 0)

    def test_const_population_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.const_population, 0)

    def test_const_shield_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.const_shield, 0)

    def test_const_sum_is_not_value_greater_than_hundred(self):
        game = Game.objects.get(pk=1)
        self.assertLessEqual(100, (game.const_missile + game.const_population +
                           game.const_shield))

    def test_time_missile_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.time_missile, 0)

    def test_initial_population_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.initial_population, 0)

    def test_can_desactivate_a_planet(self):
        user = User.objects.get(pk=1)
        game = Game.objects.get(pk=1)
        planet = Planet.objects.get(pk=1, game=game)
        self.assertTrue(game.desactivatePlanet(planet.id))

    def test_can_not_desactivate_twice_a_planet(self):
        game = Game.objects.get(pk=1)
        planet = Planet.objects.get(pk=1)
        if game.desactivatePlanet(planet.id):
            self.assertFalse(game.desactivatePlanet(planet.id))
        else:
            raise AssertionError

    def test_can_start_game(self):
        game = Game.objects.get(pk=1)
        game.startGame()
        self.assertTrue(game.game_started)

    def test_can_join_game(self):
        game = Game.objects.get(pk=1)
        user = User(username="JJJ", first_name="JJJLJH", last_name= "JJJLKGLVJ",
                    email="dv@gmail.com", password="Aa12345678")
        user.save()
        self.assertTrue(game.joinGame(user_id=user.id, name="Sion", seed=2))

    def test_can_not_twice_join_game(self):
        game = Game.objects.get(pk=1)
        user = User(username="JJJ", first_name="JJJLJH", last_name= "JJJLKGLVJ",
                    email="dv@gmail.com", password="Aa12345678")
        user.save()
        if game.joinGame(user_id=user.id, name="Sion", seed=2):
            self.assertFalse(game.joinGame(user_id=user.id, name="Sion", seed=2))
        else:
            raise AssertionError
