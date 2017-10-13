from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from game.forms import *
from django.http import HttpResponse
from game.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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

def homeView(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def joinView(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            id_partida = form.cleaned_data.get("id_partida")
            partida = Partida.objects.get(pk=id_partida)
            currentPlaying = Planet.objects.filter(gameroom=id_partida).count()
            if currentPlaying+1 > partida.max_players:
                messages.error(request, 'This game have passed the limit of players.')
            elif partida.playing == True:
                messages.error(request, 'This game is currently on a match, join another.')
            else:
                planet_name = form.cleaned_data.get("planet_name")
                userId = request.user.id
                planet = Planet(gameroom_id=id_partida, name=planet_name, player_id=userId)
                planet.save()
                return HttpResponseRedirect('/lobby/')
    else:
        form = JoinForm()
    return render(request, 'joinform.html', {'form': form})


@login_required
def gameRoomsView(request):
    template = loader.get_template('gamerooms.html')
    context = {}
    return HttpResponse(template.render(context,request))