from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import *
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
        self.assertTemplateUsed("game_rooms.html") #Template used for successfull login

    def test_bad_login(self):
        response = self.client.post('/login/', username='notexist', password='123')
        self.assertFalse(response.context['user'].is_active)

    def test_game_rooms_after_login(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('game_rooms'))
        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        #Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        #Check we used correct template
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
        """Create user"""
        self.credentials = {
            'username': 'testuser',
            'password': '12345'}
        test_user1 = User.objects.create_user(**self.credentials)
        test_user1.save()

    def


class OtherViewsTest(TestCase):
    def test_instructions(self):
        c = Client()
        c.get("/game_instructions")
        self.assertTemplateUsed("game_instructions.html")

    def test_home(self):
        c = Client()
        c.get("/")
        self.assertTemplateUsed("home.html")

