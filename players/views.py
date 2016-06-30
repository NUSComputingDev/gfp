from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q, F, Sum
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

from players.models import Player
from scoreboard.forms import PointCodeForm
from scoreboard.models import Game, GameSession


def index(request):
    if not request.user.is_authenticated():
        return redirect('players:players-login')
    elif not hasattr(request.user, 'player'):
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            logout(request)
            messages.error(request, 'You are not a participant for this year\'s party.')
            return redirect('players:players-login')
    else:
        player = Player.objects.get(user=request.user)
        scores = player.score_set.all().filter(Q(game_session__game__display_leaderboard=True) |
                                               Q(game_session__isnull=True))\
                                       .values('game_session__game')\
                                       .annotate(total_score=Sum(F('score')), name=F('game_session__game__name'))

        total_score = sum(score['total_score'] for score in scores)

        active_guessing_games = GameSession.objects.filter(game__game_type=Game.GUESSING, is_active=True)

        pointcode_form = PointCodeForm()

        return render(request, 'players/index.html', {'player': player, 'scores': scores, 'total': total_score,
                                                      'guessing_games': active_guessing_games,
                                                      'pointcode_form': pointcode_form})

def login_view(request):
    form = AuthenticationForm()

    if request.user.is_authenticated():
        return redirect('players-index')

    if request.POST:
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('players-index')

    return render(request, 'players/login.html', {'form': form})
