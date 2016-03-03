from django.shortcuts import render
from .models import Game

# Create your views here.
def scoreboard_view(request):
	games = Game.objects.all()
	return render(request, 'scoreboard/scoreboard.html', {'games': games})
