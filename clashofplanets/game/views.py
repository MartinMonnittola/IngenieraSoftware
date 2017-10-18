# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from game.forms import *
from game.models import *
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from random import randint
import random
import math
import json

# Create your views here.
class Login(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url =  reverse_lazy('game_rooms')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def homeView(request): # Main View
    template = loader.get_template('home.html')
    context={}
    return HttpResponse(template.render(context, request))

def signupView(request): # Sign Up View (Allow Users to register on system)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def gameInstructionsView(request): # game instructions View
    template = loader.get_template('game_instructions.html')
    context={}
    return HttpResponse(template.render(context, request))

class gameRoomsListView(TemplateView):
    template_name = 'game_rooms.html'
    def get(self, request, *args, **kwargs):
        latest_game_list = Room.objects.filter(game_started=0).order_by('-pub_date')
        game_form = gameForm(self.request.GET or None)
        join_form = joinForm(self.request.GET or None)
        context = {
            'latest_game_list': latest_game_list,
            'game_form': game_form,
            'join_form': join_form,
        }
        request.session['gameEntry']="na"
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):

        return HttpResponseRedirect('/game_rooms/')

@login_required
def game_closed(request):
    template = loader.get_template('gameclosed.html')
    context={}
    return HttpResponse(template.render(context, request))

@login_required
def gameRoom(request, game_room_num):
    test=request.session['gameEntry']
    if test==int(game_room_num):
        g=Room.objects.filter(id=game_room_num) #Game ID =/= Game room num, find the game that has the same room num
        planets = Planet.objects.filter(gameroom=g) #Using g, we can find the players in the game properly since game compares id's
        game=get_object_or_404(g)
        template = loader.get_template('gameroom.html')
        context = {'planets': planets,'game': game,}
        return HttpResponse(template.render(context,request))
    else:
        template = loader.get_template('badjoin.html')
        context = {}
        return HttpResponse(template.render(context, request))

@login_required
def make_player(request): #join game
    if (request.method=='POST' and request.is_ajax()):
        # gets form data
    	form = gameForm(request.POST) #gets the values submitted in the template
        planet_name=request.POST.get('pname')
        game_room_num=request.POST.get('num')
        #isolates the already existing game
        gamelist = Room.objects.filter(id=game_room_num)
        g=get_object_or_404(gamelist)
        #game doesn't exist, stop joining
        if not gamelist:
            #gameNumber = -1 indicates game doesn't exist
            data={'gameNumber':-1}
            return HttpResponse(json.dumps(data),content_type='application/json')
        #game hasn't started and players < max players
        if (int(g.game_started)==0) and (g.connected_players < g.max_players):
            #seed will be used for randomization
            seed=randint(1,90001)
            # creates the planet for player
            p=Planet.create(request.user, g, planet_name, seed)
            # +1 to room connected players
            g.connected_players += 1
            #save changes to actual game
            g.save()
            #creates planet with game among other things
            p.save()
            # session seed to identify planet
            request.session['id']=seed
            #Adds a cookie/session to indicate a legit entry
            request.session['gameEntry']=int(game_room_num)
            data={'gameNumber':game_room_num}
            return HttpResponse(json.dumps(data),content_type='application/json')
        elif (int(g.game_started)==0) and (g.connected_players == g.max_players):
            # game is full
            data={'gameNumber':-2}
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            #game has already started, send to sorry page
            data={'gameNumber':0}
            return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        form = gameForm()
        #Redirects to game room
        return HttpResponseRedirect('%s' % game_num)

@login_required
def make_game(request):
    #create game
    if (request.method=='POST' and request.is_ajax()):
        # form related stuff, gets data submitted in the template
        form = gameForm(request.POST)
        planet_name=request.POST.get('pname')
        room_name=request.POST.get('rname')
        max_players=request.POST.get('max_players')
        #gets all existing game rooms
        gamelist = Room.objects.all()
        #creates game
        g=Room.create(request.user, room_name, max_players)
        # +1 to room connected players
        g.connected_players += 1
        g.save()
        game_id = g.id
        # create planet
        seed=randint(1,90001)
        p=Planet.create(request.user, g, planet_name, seed)
        p.save() #creates player
        request.session['id']=seed #to identify player
        request.session['gameEntry']=int(game_id)
        data={'gameNumber': game_id}
    else:
        print("ohno")
        form = gameForm()
    return HttpResponse(json.dumps(data),content_type='application/json')

#send a list of players as a json to js file
def send_players(request):
	if (request.method=='POST' and request.is_ajax()):
		game_num=request.POST.get('game_num')
		g=Room.objects.filter(id=game_num)
		planets = Planet.objects.filter(gameroom=g) #players in game
		plist=[]
		for planet in planets:
			plist.append(planet.name)
		data={'planets':plist}
		return HttpResponse(json.dumps(data),content_type='application/json')

#send a list of numbers of all open games as a json to js file
def send_games(request):
	if (request.method=='POST' and request.is_ajax()):
		games=Room.objects.filter(game_started=0) #all open games
        gdict={}
        glist=[]
        for tmpgame in games:
            game_name = tmpgame.room_name
            game_max_players = tmpgame.max_players
            game_id = tmpgame.id
            game_connected_players = tmpgame.connected_players
            record = {
                'name': game_name,
                'max_players': game_max_players,
                'connected_players': game_connected_players,
                'id': game_id,
            }
            glist.append(record)
        gdict={'games': glist}
        return HttpResponse(json.dumps(gdict),content_type='application/json')

#in game
def start_game(request, game_num):
	g=Room.objects.filter(id=game_num).first()
	planets = Planet.objects.filter(game=g).order_by('seed') #players in game, sorted
	if int(g.game_started)==0: #first person to press start game
		g.game_started=1
		g.save()
	our_seed = request.session['id']
	your_guy=Player.objects.filter(seed=our_seed).first()
	template = loader.get_template('ingame.html')
	context = {
		'players': players,
		'your_guy': your_guy,
		'game': game_num,
	}
	return HttpResponse(template.render(context,request))
