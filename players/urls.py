from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^login$', views.login_view, name="players-login"),
    url(r'^logout$', auth_views.logout, name="players-logout")
]
