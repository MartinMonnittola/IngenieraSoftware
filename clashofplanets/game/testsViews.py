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
        self.assertTemplateUsed("game_rooms.html")  # Template used for successful login

    def test_bad_login(self):
        response = self.client.post('/login/', username='notexist', password='123')
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
        c.get("/signup/")
        self.assertTemplateUsed("signup.html")

    def test_signup_view_after_login(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class GameRoomsListViewTest(TestCase):
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

        self.client.login(**self.credentials1)  # testuser1 with id 1 is logged in

    @staticmethod
    def create_games():
        """
        Create some games for listing, owners are testuser2 and testuser3, so testuser1 can join
        """
        game1 = Game(game_name="Game1", max_players=10, user_id=1, pub_date=timezone.now())
        game1_owner_planet = Planet(name="Planet1", seed="1234", game_id=1, player_id=2)
        game1_owner_planet.save()
        game1.save()
        game2 = Game(game_name="Game2", max_players=7, user_id=2, pub_date=timezone.now())
        game2_owner_planet = Planet(name="Planet2", seed="12345", game_id=2, player_id=3)
        game2_owner_planet.save()
        game2.save()

    def test_no_games(self):
        response = self.client.get('/game_rooms/')
        self.assertContains(response, "No available games")

    def test_list_games(self):
        self.create_games()
        response = self.client.get('/game_rooms/')
        self.assertEqual(response.context["latest_game_list"].__len__(), 2)

    def test_create_game(self):
        data = {
            'pname': 'Planet1',
            'rname': 'Room1',
            'max_players': 10
        }

        response = self.client.post('/game_rooms/make_game/', data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Planet.objects.count(), 1)
        self.assertEqual(data["gameNumber"], 1)

    def test_bad_request_create(self):
        response = self.client.get('/game_rooms/make_game/')
        self.assertEqual(response.status_code, 400)

    def test_join_game(self):
        self.create_games()
        data = {
            'pname': 'Planet3',
            'num': 1,
        }
        response = self.client.post('/game_rooms/make_player/', data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        data = json.loads(response.content)
        self.assertEqual(Planet.objects.count(), 3)
        self.assertEqual(Planet.objects.get(pk=3).name.__str__(), "Planet3")
        self.assertEqual(data["gameNumber"], '1')


class OtherViewsTest(TestCase):
    def test_instructions(self):
        c = Client()
        c.get("/game_instructions")
        self.assertTemplateUsed("game_instructions.html")

    def test_home(self):
        c = Client()
        c.get("/")
        self.assertTemplateUsed("home.html")
