"""
Game Views
"""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from game.forms import *
from game.models import *
from random import *
from haikunator import Haikunator

# Create your views here.

class Login(FormView):
    """
    Login View
    """
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('game_rooms')

    def dispatch(self, request, *args, **kwargs):
        """
        Method that redirects to game_rooms when logged in
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Method that checks for a valid form
        """
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


# Main View
def home_view(request):
    """
    Home view template render
    """
    return render(request, 'home.html')


# Sign Up View (Allow Users to register on system)
def signup_view(request):
    """
    Sign Up View
    """
    if not request.user.is_authenticated:
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
    return HttpResponseRedirect('/')


def game_instructions_view(request):
    """
    Render instructions view
    """
    return render(request, 'game_instructions.html')


# game room list view
@login_required
def game_status(request, game_num):
    """
    Render finished game stats view
    """
    planet_user = Planet.objects.get(player=request.user, game=game_num)
    game = Game.objects.get(pk=game_num)
    planets = Planet.objects.filter(game=game)
    missiles_created = Missile.objects.filter(owner=planet_user).count()
    missiles_used = Missile.objects.filter(owner=planet_user, is_active=False).count()
    plist = []
    for p in planets:
        missiles = {
            'planet': p,
            'missiles_created': Missile.objects.filter(owner=p).count(),
            'missiles_used': Missile.objects.filter(owner=p).count()
        }
        plist.append(missiles)
    context = {'planets': planets,'planet_user': planet_user,'game': game,'plist': plist}
    if game.num_alliances >= 2:
        alliance_user = Alliance.objects.get(name=planet_user.alliance)
        context['alliance_user'] = alliance_user
        print alliance_user
    return render(request, 'game_stats.html', context)

# game room list view
@method_decorator(login_required, name='dispatch')
class GameRoomsListView(TemplateView):
    """List available games"""
    template_name = 'game_rooms.html'

    def get(self, request, *args, **kwargs):
        """
        GameRoomsList get method
        """
        game_list = Game.objects.filter(game_started=0).order_by('-pub_date')
        paginator = Paginator(game_list, 10)
        page = request.GET.get('page')
        try:
            latest_game_list = paginator.page(page)
        except PageNotAnInteger:
            latest_game_list = paginator.page(1)
        except EmptyPage:
            latest_game_list = paginator.page(paginator.num_pages)
        if page is None:
            game_form = gameForm(self.request.GET or None)
            join_form = joinForm(self.request.GET or None)
        else:
            game_form = gameForm()
            join_form = joinForm()
        context = {
            'latest_game_list': latest_game_list,
            'game_form': game_form,
            'join_form': join_form,
        }
        return self.render_to_response(context)

    @staticmethod
    def post(request):
        """
        GameRoomsList post method
        """
        return HttpResponseRedirect('/game_rooms/')


# game room close view
@login_required
def game_closed(request):
    """
    Game close view
    """
    return render(request, 'gameclosed.html')


# game room inside view
@login_required
def game_room(request, game_num):
    """
    Room view after join
    :param request: Request Object
    :param game_num: Number of game
    :return: HTTPResponse Object
    """
    # Game ID =/= Game room num, find the game that has the same room num
    g = Game.objects.filter(id=game_num)
    # Using g, we can find the players in the game properly since game compares
    #  id's
    planets = Planet.objects.filter(game=g)
    game = get_object_or_404(g)
    context = {'planets': planets, 'game': game, 'gameid': str(game.id)}
    return render(request, 'gameroom.html', context)


# join game room
@login_required
def make_player(request):
    """
    Join a game
    :param request: Request Object
    :return: JSON Response
    """
    if request.method == 'POST' and request.is_ajax():
        # gets the values submitted in the from at template
        planet_name = request.POST.get('pname')
        game_room_num = int(request.POST.get('num'))
        # isolates the already existing game
        gamelist = Game.objects.filter(id=game_room_num)
        if not gamelist:
            # gameNumber = -1 indicates game doesn't exist
            data = {'gameNumber': -1}
            return JsonResponse(data, safe=False)
        g = gamelist.get()
        planet_owner = request.user.id
        planets_from_user = Planet.objects.filter(player=planet_owner,
                                                  game=g.id)
        if (int(g.game_started) == 0) and (g.connected_players < g.max_players):
            # game hasn't started and players < max players
            # seed will be used for randomization
            rseed = randint(1, 90001)
            if len(planets_from_user) == 0:
                if planet_name == "":
                    planet_name = "Planet "+request.user.username
                g.joinGame(planet_owner, planet_name, rseed)
            data = {'gameNumber': game_room_num}
            return JsonResponse(data, safe=False)
        if (int(g.game_started) == 0) and (g.connected_players == g.max_players):
            # game hasn't started and is full
            if len(planets_from_user) > 0:
                data = {'gameNumber': game_room_num}
                return JsonResponse(data, safe=False)
            else:
                data = {'gameNumber': -2}
                return JsonResponse(data, safe=False)
        else:
            # game has already started, send to sorry page
            data = {'gameNumber': 0}
            return JsonResponse(data, safe=False)
    else:
        # Redirects to lobby
        return HttpResponseRedirect('/game_rooms/')

# make game room
@login_required
def make_game(request):
    """
    Create new game
    :param request: request object
    :return: Json Response of created game
    """
    # create game
    if request.method == 'POST' and request.is_ajax():
        # form related stuff, gets data submitted in the template
        planet_name = request.POST.get("pname")
        room_name = request.POST.get("rname")
        max_players = int(request.POST.get("max_players"))
        bot_def_num = int(request.POST.get("bot_def_num"))
        bot_ofc_num = int(request.POST.get("bot_ofc_num"))
        num_alliances = int(request.POST.get("num_alliances"))
        game_mode = int(request.POST.get("game_mode"))

        if max_players < 2:
            data = {'gameNumber': -1,
                    'message': "Max_players can't be less than 2."}
        elif (max_players - 1) - (bot_def_num+bot_ofc_num) < 0:
            data = {'gameNumber': -3,
                    'message': ("Bot players can't be greater than " +
                                str(max_players - 1) + ".")}
        else:
            # creates game
            g = Game.create(request.user, room_name, max_players, num_alliances,
                            game_mode, bot_def_num, bot_ofc_num)
            g.save()
            game_id = g.id

            # random name generator for alliances
            haikunator = Haikunator()

            # create alliances
            if num_alliances >= 2:
                for i in range(num_alliances):
                    name = haikunator.haikunate(token_length=0, delimiter=' ')
                    alliance = Alliance.create(name, g)
                    alliance.save()
            else:
                alliance = Alliance.create("-", g)
                alliance.save()
            fst_alliance = Alliance.objects.filter(game=g).first()

            # game creator joins the game
            rseed = randint(1, 90001)
            planet_owner = request.user
            g.joinGame(planet_owner.id, planet_name, rseed)

            # create bots
            for num_bot in range(bot_def_num):
                alliances = Alliance.objects.filter(game=g).order_by("num_players")
                bot_alliance = alliances.first()
                seed = randint(1, 90001)
                bot = Defensive.create(g)
                # create planet.
                bot_planet = Planet.create(player = None, bot = bot, game = g,
                                           name = ('A' + str(bot.pk)),
                                           seed = seed, alliance = bot_alliance)
                bot_planet.save()
                bot_alliance.add_player()
                g.connected_players += 1
                g.save()
            for num_bot in range(bot_ofc_num):
                alliances = Alliance.objects.filter(game=g).order_by("num_players")
                bot_alliance = alliances.first()
                seed = randint(1, 90001)
                bot = Offensive.create(g)
                # create planet.
                bot_planet = Planet.create(player = None, bot = bot, game = g,
                                           name = ('A' + str(bot.pk)),
                                           seed = seed, alliance = bot_alliance)
                bot_planet.save()
                bot_alliance.add_player()
                g.connected_players += 1
                g.save()
            data = {'gameNumber': game_id}
    else:
        return HttpResponseBadRequest("Bad Request")
    return JsonResponse(data, safe=False)

# send a list of players as a json to js file
def send_planets(request, game_num):
    """
    Send list of planets
    :return: JSON Response object
    """
    if request.method == 'GET' and request.is_ajax():
        g = Game.objects.get(id=game_num)
        planets = Planet.objects.filter(game=game_num)  # players in game
        plist = []
        current_user = request.user.username
        for tmpplanet in planets:
            planet_name = tmpplanet.name
            if not (tmpplanet.player is None):
                planet_owner = tmpplanet.player
            else:
                planet_owner = tmpplanet.bot
            planet_id = tmpplanet.id
            planet_pop = tmpplanet.population_qty
            planet_shield = tmpplanet.shield_perc
            planet_is_alive = tmpplanet.is_alive
            planet_missiles = tmpplanet.missiles_qty
            planet_alliance = str(tmpplanet.alliance)
            cantidad_asig = tmpplanet.population_qty * tmpplanet.population_distr / 100.0
            calculo_generar_pop = cantidad_asig / g.const_population
            cant_asig_shield = tmpplanet.population_qty * tmpplanet.shield_distr / 100.0
            calculo_generar_shield = cant_asig_shield / g.const_shield
            cant_asig_mis = tmpplanet.population_qty * tmpplanet.missile_distr / 100.0
            calculo_generar_missile = cant_asig_mis / g.const_missile
            if isinstance(planet_owner, User):
                owner = planet_owner.username
            else:
                owner = planet_owner.name
            record = {
                'name': planet_name,
                'id': planet_id,
                'owner': owner,
                'pop': planet_pop,
                'shield': planet_shield,
                'missiles': planet_missiles,
                'alliance': planet_alliance,
                'is_alive': planet_is_alive,
                'pop_per_second': round(calculo_generar_pop/2,2),
                'shield_per_second': round(calculo_generar_shield/2,2),
                'missiles_per_second': round(calculo_generar_missile/2,2)
            }
            plist.append(record)
        pdict = {'planets': plist, 'user': current_user, 'game_status': g.game_finished}
        return JsonResponse(pdict, safe=False)

# send a list of numbers of all open games as a json to js file
def send_games(request):
    """
    Send open games
    """
    if request.method == 'GET' and request.is_ajax():
        games = Game.objects.filter(game_started=False)  # all open games
        glist = []
        for tmpgame in games:
            g_name = tmpgame.game_name
            g_max_players = tmpgame.max_players
            g_id = tmpgame.id
            g_connected_players = tmpgame.connected_players
            g_owner = tmpgame.user.username
            g_num_alliances = tmpgame.num_alliances
            record = {
                'name': g_name,
                'max_players': g_max_players,
                'owner': g_owner,
                'connected_players': g_connected_players,
                'id': g_id,
                'num_alliances': g_num_alliances,
            }
            glist.append(record)
        gdict = {'games': glist}
        return JsonResponse(gdict, safe=False)


# send the game room state of current as a json to js file
def send_game_state(request, game_num):
    """
    Send game room state
    """
    if request.method == 'GET' and request.is_ajax():
        room = Game.objects.get(pk=game_num)  # players in game
        current_room_state = room.game_started
        players_in_room = room.connected_players
        sdict = {'game_state': current_room_state,
                 'players_in_room': players_in_room}
        return JsonResponse(sdict, safe=False)


# start game view: Allows room user to start the game room
def start_game(request, game_num):
    """
    Start game view
    :param request:
    :param game_num:
    :return:
    """
    # form = attackForm(game_num)
    # gets the game by id
    g = Game.objects.get(id=game_num)
    # players in game, sorted
    planets = Planet.objects.filter(game=g.id).order_by('id')
    # set game state to 1
    if request.user.id == g.user_id:
        Game.startGame(g)
    your_planet = Planet.objects.get(player=request.user, game=g)
    context = {
        'planets': planets,
        'your_planet': your_planet,
        'game': g,
    }
    return render(request, 'ingame.html', context)


# Allow players to change their resources generation rate
def change_distribution(request, game_num):
    """
    Change distribution view
    """
    if request.method == 'POST' and request.is_ajax():
        population = int(request.POST.get('population'))
        shield = int(request.POST.get('shield'))
        missiles = int(request.POST.get('missiles'))
        planet = Planet.objects.filter(player=request.user, game=game_num)
        p = get_object_or_404(planet)
        p.assign_perc_rate(population, shield, missiles)
        p.save()
        rdict = {'pop_dis': population, 'shield_dis': shield,
                 'missile_dist': missiles}
    else:
        rdict = {'error': 'bad_request'}
    return JsonResponse(rdict, safe=False)


# Allow players to attack their enemies
def send_attack(request, game_num):
    """
    View to attack enemy planets
    """
    if request.method == 'POST' and request.is_ajax():
        # get game room data
        game = Game.objects.get(pk=game_num)
        # get planet target data
        planet_target_id = int(request.POST.get('planet_id'))
        planet_target = Planet.objects.get(pk=planet_target_id,
                                           game=game_num)
        # get planet attacker data
        planet_attacker_owner = request.user
        planet_attacker = Planet.objects.get(player=planet_attacker_owner,
                                             game=game_num)
        # attack data
        if planet_attacker.missiles_qty > 0: # planet has missiles to launch
            m = Missile.create(owner=planet_attacker,target=planet_target)
            m.save()
            planet_attacker.missiles_qty -= 1
            planet_attacker.save()
            attack_message = 1
        else:  # planet doesnt have missiles to launch
            attack_message = 0
        # send attack msg (attack ok or error)
        attack_dict = {'origin_id': planet_attacker.id,
                       'target_id': planet_target.id,
                       'message': attack_message}
    else:
        attack_dict = {'error': 'bad_request'}
    return JsonResponse(attack_dict, safe=False)


# Allow players to attack their enemies
def send_pop(request, game_num):
    """
    View to send pop to ally planets
    """
    if request.method == 'POST' and request.is_ajax():
        # get game room data
        game = Game.objects.get(pk=game_num)
        # get planet target data
        planet_target_id = int(request.POST.get('planet_id'))
        planet_target = Planet.objects.get(pk=planet_target_id,
                                           game=game_num)
        # get planet pop data
        planet_sending_owner = request.user
        planet_sending = Planet.objects.get(player=planet_sending_owner,
                                             game=game_num)
        # planet data
        send_pop_message = planet_sending.send_population(planet_target)
        send_pop_dict = {'origin_id': planet_sending.id,
                       'target_id': planet_target.id,
                       'message': send_pop_message}
    else:
        send_pop_dict = {'error': 'bad_request'}
    return JsonResponse(send_pop_dict, safe=False)


# Show destination of active missiles
def missiles_status(request, game_num):
    """
    :param request:
    :param game_num: game actually playing
    :return: Json Response with destination of active missiles
    """
    if request.method == 'GET' and request.is_ajax():
        if game_num:
            planet = Planet.objects.get(game_id=game_num,
                                        player_id=request.user.id)
            missiles = Missile.objects.filter(owner__exact=planet,
                                              is_active__exact=True)
        else:
            data = {'error': 'game_id missing'}
            return JsonResponse(data, safe=False)

        data = {}
        for missile in missiles:
            if missile.target.name in data:
                data[missile.target.name] += 1
            else:
                data[missile.target.name] = 1
        return JsonResponse(data, safe=False)
    else:
        data = {'error': 'bad_request'}

    return JsonResponse(data, safe=False)


def error_404(request):
    data = {}
    return render(request,'error_404.html', data)


def error_500(request):
    data = {}
    return render(request,'error_500.html', data)
