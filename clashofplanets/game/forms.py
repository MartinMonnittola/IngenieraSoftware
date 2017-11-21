# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from game.models import *

# Create your forms here.

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Required. It should be more than 8 characters not entirely numerical.'
        self.fields['password2'].help_text = 'Required. Write your password again.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class gameForm(forms.ModelForm):
    planet_name = forms.CharField(widget=forms.TextInput(attrs={'id':'planet_nameC', 'required': True}))
    game_name = forms.CharField(widget=forms.TextInput(attrs={'id':'game_nameC', 'required': True}))
    game_mode = forms.ChoiceField(choices=Game.MODE_CHOICES, widget=forms.Select(attrs={'id': 'game_modesC', 'required': True}))
    max_players = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'value': "",
            'id': 'max_playersC',
            'type': 'text',
            'class': 'max_playersC-slider'}
            )
        )
    num_alliances = forms.IntegerField(label='Number Of Alliances',widget=forms.NumberInput(
        attrs={
            'value': "",
            'id':'num_alliancesC',
            'type': 'text',
            'class': 'num_alliancesC-slider',}
            )
        )
    bot_players = forms.IntegerField(label='Number Of Bot Players', widget=forms.NumberInput(
        attrs={
            'value': "",
            'id':'bot_playersC',
            'type': 'text',
            'class': 'bot_playersC-slider',}
            )
        )

    DEFENSIVE = 1
    OFFENSIVE = 2
    MODE_CHOICES = (
        (DEFENSIVE, "Defensive"),
        (OFFENSIVE, "Offensive")
    )
    bot_mode = forms.ChoiceField(choices= MODE_CHOICES, required = False)

    class Meta:
        model = Game
        fields = ('game_name', 'max_players', 'num_alliances', 'bot_players') # bot_players - #game_mode

    def __init__(self, *args, **kwargs):
        super(gameForm, self).__init__(*args, **kwargs)
        self.fields['game_name'].help_text = 'Write a name for your Game. Required.'
        self.fields['max_players'].help_text = 'How many players can join your Game?. Required. Min 2 Max 50.'
        self.fields['num_alliances'].help_text = 'How many alliances will exist on your game?. Required. Min 0 Max 10.'
        self.fields['planet_name'].help_text = 'Write a name for your planet. Required'
        self.fields['bot_players'].help_text = 'How many bots do you want to be in game?. Required. Min 2 Max 10. 0 to deactivate'
        self.fields['game_mode'].help_text = 'Choose a game mode to play.'
        self.fields['bot_mode'].help_text = 'Choose the bot`s mode . No required'


class joinForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id':'planet_name', 'required': False}))
    game_id = forms.CharField(widget=forms.TextInput(attrs={'id':'game_num', 'required': True}))

    class Meta:
        model = Planet
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(joinForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Write a name for your planet. If you are already in the Game, just write the Game id. Required.'
        self.fields['game_id'].help_text = 'Write the id of the Game you want to join. Required.'
