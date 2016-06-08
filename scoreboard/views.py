from django.shortcuts import render
from .models import Game, Score
from .forms import GuessingForm
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def scoreboard_view(request):
	games = Game.objects.all()
	return render(request, 'scoreboard/scoreboard.html', {'games': games})

@login_required
def guess_view(request):
	form = GuessingForm()
	return render(request, 'scoreboard/guesser.html', {'form': form})