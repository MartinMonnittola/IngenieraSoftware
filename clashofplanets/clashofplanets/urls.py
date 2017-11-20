"""
Clash of Planets URLS
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from game.views import *
from django.contrib.auth.views import logout

app_name = 'game'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view, name='home'),
    url(r'^signup/$', signup_view, name='signup'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^game_instructions/$', game_instructions_view,
        name='game_instructions'),
    # Game Room List (Lobby):
    url(r'^game_rooms/$', GameRoomsListView.as_view(), name='game_rooms'),
    # Make game:
    url(r'^game_rooms/make_game/$', make_game, name='make_game'),
    # Makes player and games:
    url(r'^game_rooms/make_player/$', make_player, name='make_player'),
    # Actual game room, directed from make_player:
    url(r'^game_rooms/(?P<game_room_num>[0-9]+)/$', game_room,
        name='game_room'),
    url(r'^game_rooms/GameClosed/$', game_closed, name='game_closed'),
    url(r'^game_rooms/\d+/get_planets/$', send_planets, name='send_planets'),
    url(r'^game_rooms/\d+/get_game_state/$', send_game_state,
        name='send_game_state'),
    url(r'^game_rooms/get_games/$', send_games, name='send_games'),
    url(r'^game_rooms/game/(?P<game_num>[0-9]+)/$', start_game,
        name='start_game'),
    url(r'^game_rooms/game/\d+/get_planets/$', send_planets,
        name='send_planets'),
    url(r'^game_rooms/game/\d+/change_distribution/$', change_distribution,
        name='change_distribution'),
    url(r'^game_rooms/game/\d+/send_attack/$', send_attack,
        name='send_attack'),
    url(r'^game_rooms/game/\d+/send_pop/$', send_pop,
        name='send_pop'),
    url(r'^game_rooms/game/\d+/missiles_status/$', missiles_status,
        name='missiles_status'),
    url(r'^game_rooms/game/(?P<game_num>[0-9]+)/stats/$', game_status,
        name='game_status')
]
