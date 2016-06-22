from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^login$', views.login_view, name="players-login"),
]
