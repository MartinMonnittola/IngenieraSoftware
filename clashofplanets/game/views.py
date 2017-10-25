# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from game.forms import *
from game.models import *
from random import *
import math
import json

# Create your views here.

# login view
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

# Main View
def homeView(request):
    return render(request, 'home.html')

# Sign Up View (Allow Users to register on system)
def signupView(request):
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

# game instructions view
def gameInstructionsView(request):
    return render(request, 'game_instructions.html')

# game room list view
@method_decorator(login_required, name='dispatch')
class gameRoomsListView(TemplateView):
    template_name = 'game_rooms.html'
    def get(self, request, *args, **kwargs):
        latest_game_list = Game.objects.filter(game_started=0).order_by('-pub_date')
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

# game room close view
@login_required
def game_closed(request):
    return render(request, 'gameclosed.html')

# game room inside view
@login_required
def gameRoom(request, game_room_num):
    test=request.session['gameEntry']
    if test==int(game_room_num):
        g=Game.objects.filter(id=game_room_num) #Game ID =/= Game room num, find the game that has the same room num
        planets = Planet.objects.filter(game=g) #Using g, we can find the players in the game properly since game compares id's
        game=get_object_or_404(g)
        context = {'planets': planets,'game': game, 'gameid': str(game.id)}
        return render(request, 'gameroom.html', context)
    else:
        return render(request, 'badjoin.html')

#join game room
@login_required
def make_player(request):
    if (request.method=='POST' and request.is_ajax()):
        #gets the values submitted in the from at template
        form = gameForm(request.POST)
        planet_name=request.POST.get('pname')
        game_room_num=request.POST.get('num')
        #isolates the already existing game
        gamelist = Game.objects.filter(id=game_room_num)
        if not gamelist:
            #gameNumber = -1 indicates game doesn't exist
            data={'gameNumber':-1}
            return JsonResponse(data, safe=False)
        g=get_object_or_404(gamelist)
        if (int(g.game_started)==0) and (g.connected_players < g.max_players):
            #game hasn't started and players < max players
            #seed will be used for randomization
            seed=randint(1,90001)
            planet_owner = request.user.id
            planets_from_user = Planet.objects.filter(player=planet_owner, game=g.id)
            if len(planets_from_user) == 0:
                p=Planet.create(request.user, g, planet_name, seed)
                p.save() #creates player
            # session seed to identify planet
            request.session['id']=seed
            #Adds a cookie/session to indicate a legit entry
            request.session['gameEntry']=int(game_room_num)
            data={'gameNumber':game_room_num}
            return JsonResponse(data, safe=False)
        if (int(g.game_started)==0) and (g.connected_players == g.max_players):
            # game hasn't started and is full
            data={'gameNumber':-2}
            return JsonResponse(data, safe=False)
        else:
            #game has already started, send to sorry page
            data={'gameNumber':0}
            return JsonResponse(data, safe=False)
    else:
        form = gameForm()
        #Redirects to game room
        return HttpResponseRedirect('%s' % game_num)

# make game room
@login_required
def make_game(request):
    #create game
    if (request.method=='POST' and request.is_ajax()):
        # form related stuff, gets data submitted in the template
        form = gameForm(request.POST)
        planet_name=request.POST.get('pname')
        room_name=request.POST.get('rname')
        max_players=request.POST.get('max_players')
        #creates game
        g=Game.create(request.user, room_name, max_players)
        # +1 to room connected players
        g.connected_players += 1
        g.save()
        game_id = g.id
        # create planet
        seed=randint(1,90001)
        #Game.joinGame(g, request.user, planet_name, seed)
        p=Planet.create(request.user, g, planet_name, seed)
        p.save() #creates player
        request.session['id']=seed #to identify player
        request.session['gameEntry']=int(game_id)
        data={'gameNumber': game_id}
    else:
        print("ohno")
        form = gameForm()
    return JsonResponse(data, safe=False)

#send a list of players as a json to js file
def send_planets(request):
    if (request.method=='POST' and request.is_ajax()):
        game_num =request.POST.get('num')
        planets = Planet.objects.filter(game=game_num) #players in game
        pdict={}
        plist=[]
        current_user = request.user.username
        for tmpplanet in planets:
            planet_name = tmpplanet.name
            planet_owner = tmpplanet.player
            planet_id = tmpplanet.id
            planet_seed = tmpplanet.seed
            planet_pop = tmpplanet.population_qty
            planet_shield = tmpplanet.shield_perc
            planet_missiles = tmpplanet.missiles_qty
            record = {
                'name': planet_name,
                'id': planet_id,
                'seed': planet_seed,
                'owner': planet_owner.username,
                'pop': planet_pop,
                'shield': planet_shield,
                'missiles': planet_missiles,
            }
            plist.append(record)
        pdict={'planets': plist, 'user': current_user}
        return JsonResponse(pdict, safe=False)

#send a list of numbers of all open games as a json to js file
def send_games(request):
    if (request.method=='POST' and request.is_ajax()):
        games=Game.objects.filter(game_started=False) #all open games
        gdict={}
        glist=[]
        for tmpgame in games:
            g_name = tmpgame.game_name
            g_max_players = tmpgame.max_players
            g_id = tmpgame.id
            g_connected_players = tmpgame.connected_players
            g_owner = tmpgame.user.username
            record = {
                'name': g_name,
                'max_players': g_max_players,
                'owner': g_owner,
                'connected_players': g_connected_players,
                'id': g_id,
            }
            glist.append(record)
        gdict={'games': glist}
        return JsonResponse(gdict, safe=False)

#send the game room state of current as a json to js file
def send_game_state(request):
    if (request.method=='POST' and request.is_ajax()):
        game_num =request.POST.get('num')
        room = Game.objects.get(pk=game_num) #players in game
        sdict={}
        current_room_state = room.game_started
        players_in_room = room.connected_players
        sdict={'game_state': current_room_state, 'players_in_room': players_in_room,}
        return JsonResponse(sdict, safe=False)

# start game view: Allows room user to start the game room
def start_game(request, game_num):
    template = loader.get_template('ingame.html')
    #form = attackForm(game_num)
    #gets the game by id
    g=Game.objects.get(id=game_num)
    #players in game, sorted
    planets = Planet.objects.filter(game=g.id).order_by('seed')
    # set game state to 1
    Game.startGame(g)
    our_seed = request.session['id']
    your_planet=Planet.objects.get(player=request.user, game=g)
    context = {
        'planets': planets,
        'your_planet': your_planet,
        'game': game_num,
        #'attack_form': form,
        }
    return render(request, 'ingame.html', context)

# Allow players to change their resources generation rate
def change_distribution(request):
    if request.method=='POST' and request.is_ajax():
        game_num=int(request.POST.get('game_num'))
        population=int(request.POST.get('population'))
        shield=int(request.POST.get('shield'))
        missiles=int(request.POST.get('missiles'))
        planet=Planet.objects.filter(player=request.user, game=game_num)
        p=get_object_or_404(planet)
        p.assign_perc_rate(population, shield, missiles)
        p.save()
        rdict = {'pop_dis': population, 'shield_dis': shield, 'missile_dist': missiles}
    return JsonResponse(rdict, safe=False)

# Allow players to attack their enemies
def send_attack(request):
    if request.method=='POST' and request.is_ajax():
        planet_gameroom = int(request.POST.get('game_num'))
        planet_id = int(request.POST.get('planet_id'))
        planet=Planet.objects.filter(pk=planet_id, game=planet_gameroom)
        p=get_object_or_404(planet)
        p.population_qty -= 100
        p.save()
        rdict = {'planet_id': planet_id}
    return JsonResponse(rdict, safe=False)
