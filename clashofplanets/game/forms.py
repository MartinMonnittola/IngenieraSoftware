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
    room_name = forms.CharField(widget=forms.TextInput(attrs={'id':'room_nameC', 'required': True}))
    max_players = forms.IntegerField(widget=forms.NumberInput(attrs={'id':'max_playersC', 'required': True}))

    class Meta:
        model = Room
        fields = ('room_name', 'max_players') # bot_players - #game_mode

    def __init__(self, *args, **kwargs):
        super(gameForm, self).__init__(*args, **kwargs)

class joinForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id':'planet_name', 'required': True}))
    room_id = forms.CharField(widget=forms.TextInput(attrs={'id':'room_num', 'required': True}))

    class Meta:
        model = Planet
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(joinForm, self).__init__(*args, **kwargs)
