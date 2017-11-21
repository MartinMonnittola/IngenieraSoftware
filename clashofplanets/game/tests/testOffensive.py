from django.test import TestCase
from game.models import *

class OffensiveModelTestsCase(TestCase):

    def setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()

        game = Game.create(name = "GuerraPlanetaria", max_players = 20,
                           owner = user, num_alliances = 2, mode=1, bot_def=0, bot_ofc=1)
        game.save()

        allianceb = Alliance.create(name = "Blanco", game = game)
        alliancen = Alliance.create(name = "Negro", game = game)
        allianceb.save()
        alliancen.save()

        bot = Offensive(name="BotA", probability_attack = 30,
                        probability_modify_resources = 60,
                        probability_send_population = 60
                        )
        bot.save()

        planet = Planet.create(player = None, bot=bot, game = game, name = "Tierra",
                               seed =1, alliance = allianceb)
        planet.save()
        allianceb.add_player()

    def test_name_equal_bot_pk(self):
        """
        Prueba si el nombre del Bot creado con el metodo create es igual a la
        palabra "Bot" concatenado con la clave primaria del bot creado por este
        metodo.
        """
        game = Game.objects.get(pk=1)
        try:
            max_pk = Bot.objects.all().order_by("-pk").first().pk
            max_pk = max_pk + 1
        except:
            max_pk = 1
        bot = Bot.create(game)
        self.assertGreaterEqual(bot.name, ("Bot" + str(max_pk)))
