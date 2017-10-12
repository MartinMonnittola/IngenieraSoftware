from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from game.views import *
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static

app_name = 'game'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', signupView, name='signup'),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^$',views.index,name='index'),
    url(r'game',include('game.urls'))
]
