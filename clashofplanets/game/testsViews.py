"""
Views Tests
"""
from django.test import TestCase, Client
from django.urls import reverse
import json
from .forms import *

# Create your tests here.


class LoginAndSignUpViewTest(TestCase):
    def setUp(self):
        """Create user"""
        self.credentials = {
            'username': 'testuser',
            'password': '12345'}
        test_user1 = User.objects.create_user(**self.credentials)
        test_user1.save()

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        # Template used for successful login
        self.assertTemplateUsed(response, "game_rooms.html")

    def test_bad_login(self):
        response = self.client.post('/login/',
                                    username='notexist', password='123')
        self.assertFalse(response.context['user'].is_active)

    def test_game_rooms_after_login(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('game_rooms'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'game_rooms.html')

    def test_game_rooms_not_logged_redirect(self):
        c = Client()
        response = c.get("/game_rooms/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/game_rooms/')

    def test_signup_view_not_logged(self):
        c = Client()
        response = c.get("/signup/")
        self.assertTemplateUsed(response, "register.html")

    def test_signup_view_after_login(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class GameRoomsListJoinCreateViewTest(TestCase):
    def setUp(self):
        """
        Create users
        """
        self.credentials1 = {
            'username': 'testuser1',
            'password': '12345'}
        test_user1 = User.objects.create_user(**self.credentials1)
        test_user1.save()
        self.credentials2 = {
            'username': 'testuser2',
            'password': '12345'}
        test_user2 = User.objects.create_user(**self.credentials2)
        test_user2.save()
        self.credentials3 = {
            'username': 'testuser3',
            'password': '12345'}
        test_user3 = User.objects.create_user(**self.credentials3)
        test_user3.save()

        # testuser1 with id 1 log in
        self.client.login(**self.credentials1)

    @staticmethod
    def create_games():
        """
        Create some games for listing, owners are testuser2 and testuser3,
        so testuser1 can join
        """
        game1 = Game.create(User.objects.get(pk=2), "Game1", 10)
        game1.save()
        alliance1 = Alliance.create("Alliance1", Game.objects.get(pk=1))
        alliance1.save()
        planet1 = Planet.create(User.objects.get(pk=2), Game.objects.get(pk=1),
        						"Planet1", 123456, Alliance.objects.get(pk=1))
        planet1.save()
        game2 = Game.create(User.objects.get(pk=3), "Game2", 10)
        game2.save()
        alliance2 = Alliance.create("Alliance2", Game.objects.get(pk=2))
        alliance2.save()
        planet2 = Planet.create(User.objects.get(pk=3), Game.objects.get(pk=2),
        						"Planet2", 1234532, Alliance.objects.get(pk=2))
        planet2.save()

    def test_no_games(self):
        response = self.client.get('/game_rooms/')
        self.assertContains(response, "No available games")

    def test_list_games(self):
        self.create_games()
        response = self.client.get('/game_rooms/')
        self.assertEqual(response.context["latest_game_list"].__len__(), 2)
        self.assertTemplateUsed(response, 'game_rooms.html')

    def test_create_game(self):
        data = {
            'pname': 'Planet1',
            'rname': 'Room1',
            'max_players': 10,
            'num_alliances': 2,
            'bot_players': 0
        }

        response = self.client.post(
            '/game_rooms/make_game/',
            data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get(pk=1).connected_players, 1)
        self.assertEqual(Planet.objects.count(), 1)
        self.assertEqual(data["gameNumber"], 1)

    def test_create_game_incorrect_max_players(self):
        data = {
            'pname': 'Planet1',
            'rname': 'Room1',
            'max_players': -10,
            'num_alliances': 2,
            'bot_players': 0
        }

        response = self.client.post(
            '/game_rooms/make_game/',
            data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(Planet.objects.count(), 0)
        self.assertEqual(data["gameNumber"], -1)

    def test_bad_request_create(self):
        response = self.client.get('/game_rooms/make_game/')
        self.assertEqual(response.status_code, 400)

    def test_join_game(self):
        self.create_games()
        data = {
            'pname': 'Planet3',
            'num': 1,
        }
        response = self.client.post(
            '/game_rooms/make_player/',
            data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Planet.objects.count(), 3)
        self.assertEqual(Game.objects.get(pk=1).connected_players, 2)
        self.assertEqual(Planet.objects.get(pk=3).name.__str__(), "Planet3")
        self.assertEqual(data["gameNumber"], 1)

    def test_join_game_full(self):
        game = Game.create(User.objects.get(pk=2), "Game", 2)
        game.save()
        game.joinGame(3, "Planet2", 12345)
        data = {
            'pname': 'Planet3',
            'num': 1,
            'num_alliances': 2
        }
        response = self.client.post(
            '/game_rooms/make_player/',
            data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        # Game number equals -2 means Full Room
        self.assertEqual(data["gameNumber"], -2)


class InGameViewsTest(TestCase):
    def setUp(self):
        """
        Create users
        """
        self.credentials1 = {
            'username': 'testuser1',
            'password': '12345'}
        test_user1 = User.objects.create_user(**self.credentials1)
        test_user1.save()
        self.credentials2 = {
            'username': 'testuser2',
            'password': '12345'}
        test_user2 = User.objects.create_user(**self.credentials2)
        test_user2.save()
        # testuser1 with id 1 log in
        self.client.login(**self.credentials1)

    @staticmethod
    def create_game_and_planets():
        """
        Create some games with planets joined
        """
        game1 = Game.create(User.objects.get(pk=1), "Game1", 10)
        game1.save()
        alliance1 = Alliance.create("Alliance1", Game.objects.get(pk=1))
        alliance1.save()
        planet1 = Planet.create(User.objects.get(pk=1), Game.objects.get(pk=1),
        						"Planet1", 123456, Alliance.objects.get(pk=1))
        planet1.save()
        game1.joinGame(2, "Planet2", 12345)
        game1.joinGame(3, "Planet3", 123345)
        game1.joinGame(4, "Planet4", 123451)
        game1.joinGame(5, "Planet5", 123454)
        game1.joinGame(6, "Planet6", 1234512)

    def test_send_planets_as_json(self):
        self.create_game_and_planets()
        data = {
            'num': 1
        }
        response = self.client.get(
            '/game_rooms/1/get_planets/', data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Planet.objects.filter(game_id=1).count(),
                         len(data["planets"]))

    def test_send_game_state_as_json(self):
        self.create_game_and_planets()
        data = {
            'num': 1
        }
        response = self.client.get(
            '/game_rooms/1/get_game_state/', data,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Game.objects.get(pk=1).game_started,
                         data["game_state"])
        self.assertEqual(Game.objects.get(pk=1).connected_players,
                         data["players_in_room"])

    def test_game_started(self):
        self.create_game_and_planets()
        response = self.client.get('/game_rooms/game/1/')
        self.assertTrue(Game.objects.get(
            pk=response.context["game"]).game_started)
        self.assertTemplateUsed(response, "ingame.html")


class OtherViewsTest(TestCase):
    def test_instructions(self):
        c = Client()
        response = c.get("/game_instructions/")
        self.assertTemplateUsed(response, "game_instructions.html")

    def test_home(self):
        c = Client()
        response = c.get("/")
        self.assertTemplateUsed(response, "home.html")
