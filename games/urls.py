from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^draw/(?P<game_id>[0-9]+)$', views.draw_view, name="draw"),
]
