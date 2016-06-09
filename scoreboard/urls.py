from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.scoreboard_view),
    url(r'^guessing-(?P<id>[0-9]+)$', views.guess_view, name='guessing-form'),
]
