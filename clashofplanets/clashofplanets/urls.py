from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from game.views import *
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static

app_name = 'game'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', signupView, name='signup'),
    url(r'^game_instructions/$', gameInstructionsView, name='game_instructions'),
    url(r'^$', homeView, name='home'),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^game_rooms/$',joinView, name='game_rooms'),
]
