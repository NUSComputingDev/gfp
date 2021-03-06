from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^scoreboard$', views.scoreboard_view, name='scoreboard'),
    url(r'^guessing/(?P<id>[0-9]+)$', views.guess_view, name='guessing-form'),
    url(r'^redeem$', views.redemption_view, name='redemption')
]
