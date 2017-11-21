from django.test import TestCase
from .forms import * 


class GameFormTestsCase(TestCase):

    def test_form_field_bot_def_num_do_not_accept_values_negatives(self):
        form_data = {"planet_name":"fgh", "game_name": "ggdf", "game_mode":1, "max_players":20, 
                     "num_alliances": 3, "bot_def_num": -1,"bot_ofc_num": 2}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_field_bot_ofc_num_do_not_accept_values_negatives(self):
        form_data = {"planet_name":"fgh", "game_name": "ggdf", "game_mode":1, "max_players":20, 
                     "num_alliances": 3, "bot_def_num": 1,"bot_ofc_num": -2}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())


    def test_form_field_max_player_does_not_accept_value_negative_or_zero(self):
        form_data =  {"planet_name":"fgh", "game_name": "ggdf", "game_mode":1, "max_players":-20, 
                     "num_alliances": 3, "bot_def_num": 1,"bot_ofc_num": 2}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_field_game_name_does_not_accept_value_empty(self):
        form_data =  {"planet_name":"fgh", "game_name": "", "game_mode":1, "max_players":20, 
                     "num_alliances": 3, "bot_def_num": 1,"bot_ofc_num": 2}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_field_planet_name_does_not_accept_value_empty(self):
        form_data =  {"planet_name":"", "game_name": "jbh", "game_mode":1, "max_players":20, 
                     "num_alliances": 3, "bot_def_num": 1,"bot_ofc_num": 2}
        form = gameForm(form_data)
        self.assertFalse(form.is_valid())
