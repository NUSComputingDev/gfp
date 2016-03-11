from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.scoreboard_view),
    url(r'updater/', views.scoreboard_update),
]
