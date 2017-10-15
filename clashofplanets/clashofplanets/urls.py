from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from game.views import *
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static

app_name = 'game'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homeView, name='home'),
    url(r'^signup/$', signupView, name='signup'),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^game_instructions/$', gameInstructionsView, name='game_instructions'),
    url(r'^game_rooms/$', gameRoomsListView, name='game_rooms'), #Game Room List (Lobby)
    url(r'^game_rooms/make_game/$', make_game, name='make_game'), #make game, generate room_num
    url(r'^game_rooms/make_player/$', make_player, name='make_player'), #makes player and game
    url(r'^game_rooms/(?P<game_room_num>[0-9]+)/$', gameRoom, name='game_room'), #Actual game room, directed from make_player
    url(r'^game_rooms/gameclosed/$', game_closed, name='game_closed'),
    url(r'^game_rooms/\d+/GetPlayers/$', send_players, name ='send_players'),
    url(r'^game_rooms/GetGames/$', send_games, name ='send_games'),
    #url(r'^game_rooms/(?P<game_num>[0-9]+)/(?P<your_guy>[0-9]+)/$', start_game, name='start_game')
]
