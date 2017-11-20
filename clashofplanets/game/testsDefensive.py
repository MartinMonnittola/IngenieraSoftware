from django.test import TestCase
from .models import *


class DefensiveModelTestsCase(TestCase):

    def setUp(self):
        bot = Defensive(name="BotA", probability_attack = 30, 
                        probability_modify_resources = 60,
                        probability_send_population = 60
                        )
        bot.save()

    """ 
    Metodos para realizar el testeo de la aplicacion.
    """
    def test_probability_attack_has_not_value_greater_than_thirty(self):
        game = Bot.objects.get(pk=1)
        self.assertLessEqual(game.probability_attack, 30)

    def test_probability_send_population_has_not_value_greater_than_fifty(self):
        game = Bot.objects.get(pk=1)
        self.assertGreaterEqual(game.probability_send_population, 50)
