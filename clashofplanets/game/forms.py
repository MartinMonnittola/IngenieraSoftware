# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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
    planet_name = forms.CharField(label='Your planet name', max_length=20)
    game = forms.IntegerField()
    class Meta:
        model = Room
        fields = ('id','room_name', 'max_players', 'bot_players', 'missile_delay',
        'init_population', 'const_population', 'const_shield',
        'const_missile', 'population_damage_per_missile',
        'shield_damage_per_missile',)

    def __init__(self, *args, **kwargs):
        super(gameForm, self).__init__(*args, **kwargs)
        self.fields['room_name'].required = True
        self.fields['room_name'].widget.attrs['required'] = 'required'


class CreateGame(forms.ModelForm):
    """
    Form that allow players to create game rooms.
    """

    class Meta:
        model = Room
        widgets = {'user': forms.HiddenInput()}
        exclude = ['playing']

    def save(self, *args, **kwargs):
        const_poblation = self.cleaned_data.get('const_poblation')
        const_misil = self.cleaned_data.get('const_misil')
        const_shield = self.cleaned_data.get('const_shield')
        if ((const_poblation + const_misil + const_shield) == 100):
            nuevo_game = super(CreateGame, self).save(*args, **kwargs)
            nuevo_game.const_poblation = const_poblation
            nuevo_game.const_shield = const_shield
            nuevo_game.const_misil = const_misil
            nuevo_game.save()
        else:
            raise forms.ValidationError(u'Los pocentajes ingresados son incorrectos.')
