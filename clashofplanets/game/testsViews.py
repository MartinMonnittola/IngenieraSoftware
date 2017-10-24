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

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('game_rooms'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        #Check we used correct template
        self.assertTemplateUsed(resp, 'game_rooms.html')
