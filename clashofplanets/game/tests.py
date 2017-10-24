from django.test import TestCase

# Create your tests here.
from .models import *
from .forms import *

class GameModelTestsCase(TestCase):

    def test_setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()
        game = Game.createGame(1, 30, 30, 40, 1, 1, 1, 1, user)
        game.save()
        planet = Planet.create(user, game, "LJBKHB")
        planet.save()

    """ 
    Metodos para realizar el testeo de la aplicacion. 
    """
    def test_hurt_shield_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.hurt_to_shield, 0) 

    def test_hurt_population_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1)
        self.assertGreater(game.hurt_to_poblation, 0) 

    def test_const_missil_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1) 
        self.assertGreater(game.const_misil, 0) 

    def test_const_population_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1) 
        self.assertGreater(game.const_poblation, 0) 

    def test_const_shield_has_not_value_negative_or_zero(self):
        game = Game.objects.get(pk=1) 
        self.assertGreater(game.const_shield, 0)

    def test_const_sum_is_not_value_greater_than_hundred(self):
        game = Game.objects.get(pk=1)
        self.assertLessEqual((game.const_misil + game.const_poblation + 
                           game.const_shield), 100) 

    def test_time_misil_has_not_value_negative_or_zero(self): 
        self.assertGreater(game.time_misil, 0) 

    def test_initial_population_has_not_value_negative_or_zero(self): 
        self.assertGreater(game.initial_poblation, 0)

    def test_can_desactivate_a_planet(self):
        planet = Planet.objects.get(pk=1)
        game = Game.objects.get(pk=1)
        self.assertTrue(game.desactivatePlanet(planet.id))

    def test_can_not_desactivate_twice_a_planet(self):
        planet = Planet.objects.get(pk=1)
        game = Game.objects.get(pk=1)
        if game.desactivatePlanet(planet.id):
            self.assertFalse(game.desactivatePlanet(planet.id))
        else:
            raise AssertionError

    def test_can_start_game(self):
        game = Game.objects.get(pk=1)
        game.startGame()
        self.assertTrue(game.playing)

    def test_can_join_game(self):
        game = Game.objects.get(pk=1)
        user = User(username="JJJ", first_name="JJJLJH", last_name= "JJJLKGLVJ",
                    email="dv@gmail.com", password="Aa12345678")
        user.save()
        game.joinGame(user.id, "Sion")
        self.assertTrue(game.joinGame(user.id, "Sion"))

    def test_can_not_twice_join_game(self):
        game = Game.objects.get(pk=1)
        user = User(username="JJJ", first_name="JJJLJH", last_name= "JJJLKGLVJ",
                    email="dv@gmail.com", password="Aa12345678")
        user.save()
        if game.joinGame(user.id, "Sion"):
            self.assertFalse(game.joinGame(user.id, "Sion"))
        else:
            raise AssertionError

    def test_can_create_game():
        game = Game.createGame(1, 30, 30, 40, 1, 1, 1, 1, user)
        game.save()


class CreateGameTestsCase(TestCase):
    def test_setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()

    def test_form_field_hurt_poblation_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid())

    def test_form_field_hurt_shield_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"initial_poblation": 1, "const_misil":30,
                      "const_shield":30, "const_poblation":40,
                      "time_misil":1, "hurt_to_poblation":1,
                      "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid())

    def test_form_field_const_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid())

    def test_const_sum_is_not_value_greater_than_hundred(self):
        # Suponemos que las constantes ingresadas respetan los tipos de valores
        # respectivos.
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        if form.is_valid():            
            self.assertLessEqual((form_data["const_misil"] + 
                                  form_data["const_poblation"] + 
                                  form_data["const_shield"]), 100) 
        else:
            raise AssertionError

    def test_form_field_time_misil_does_not_value_negative_or_zero(self): 
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid())

    def test_form_field_initial_poblation_does_not_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data =  {"initial_poblation": 1, "const_misil":30,
                     "const_shield":30, "const_poblation":40,
                  "time_misil":1, "hurt_to_poblation":1,
                  "hurt_to_shield":1, "max_players":20, "user":user}
        form = CreateGame(form_data)
        self.assertTrue(form.is_valid())
