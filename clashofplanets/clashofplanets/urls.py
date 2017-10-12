from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from game.views import *
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static

app_name = 'game'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', signupView, name='signup')
]
