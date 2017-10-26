from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import *
from .forms import *

# Create your tests here.

class LoginAndSignUpViewTest(TestCase):
    def setUp(self):
        """Create two users"""
        self.credentials1 = {
            'username': 'testuser1',
            'password': '12345'}
        self.credentials2 = {
            'username': 'testuser2',
            'password': '12345'}
        test_user1 = User.objects.create_user(**self.credentials1)
        test_user1.save()
        test_user2 = User.objects.create_user(**self.credentials2)
        test_user2.save()

    def test_login(self):
        response = self.client.post('/login/', self.credentials1, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertTemplateUsed("game_rooms.html") #Template used for successfull login

    def test_bad_login(self):
        response = self.client.post('/login/', username='notexist',password='123')
        self.assertFalse(response.context['user'].is_active)

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


class OtherViewsTest(TestCase):
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

