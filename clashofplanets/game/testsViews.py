from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import *
from .forms import *

# Create your tests here.

class ViewsTest(TestCase):
    def setUp(self):
        #Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

    def test_instructions(self):
        c = Client()
        response = c.get("/game_instructions")
        self.assertTemplateUsed("game_instructions.html")

    def test_home(self):
        c = Client()
        response = c.get("/")
        self.assertTemplateUsed("home.html")

    def test_game_rooms_after_loggin(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('game_rooms'))
        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
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
        response = c.get("/signup/")
        self.assertTemplateUsed("signup.html")

    def test_signup_view_after_loggin(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

