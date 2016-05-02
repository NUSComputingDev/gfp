from django.shortcuts import render
from .models import Game, Score
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def scoreboard_view(request):
	games = Game.objects.all()
	return render(request, 'scoreboard/scoreboard.html', {'games': games})
