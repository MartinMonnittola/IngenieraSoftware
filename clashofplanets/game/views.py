from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from game.forms import *
from django.http import HttpResponse
from game.models import *
from django.contrib.auth.decorators import login_required


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
            planet = Planet(game_id=form.id_partida, name=form.planet_name, player_id=request.user.id)
            planet.save()
            return HttpResponseRedirect('/lobby/')
    else:
        form = JoinForm()

    return render(request, 'joinform.html', {'form': form})