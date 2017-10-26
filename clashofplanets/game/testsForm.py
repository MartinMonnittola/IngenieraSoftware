from django.test import TestCase
from .forms import * 


class GameFormTestsCase(TestCase):
    def setUp(self):
        user = User(username="GGG", first_name="GGGLJH", last_name= "GGGLKJLVG",
                    email="dvdfv@gmail.com", password="Aa12345678")
        user.save()

    def test_form_field_max_player_does_not_accept_value_negative_or_zero(self):
        user = User.objects.get(pk=1)
        form_data = {"game_name": "ghnfcg", "max_players":-20, "planet_name":"dbfgbdfgb"}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_field_game_name_does_not_accept_value_empty(self):
        user = User.objects.get(pk=1)
        form_data = {"game_name": "", "max_players":20, "planet_name":"dbfgbdfgb"}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_field_planet_name_does_not_accept_value_empty(self):
        user = User.objects.get(pk=1)
        form_data = {"game_name": "ggdf", "max_players":20, "planet_name":""}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())
