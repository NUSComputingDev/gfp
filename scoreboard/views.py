from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from players.models import Player
from games.models import Guess

from .models import Game, Score, GameSession, PointCode
from .forms import GuessingForm, PointCodeForm


@login_required
def scoreboard_view(request):
    games = Game.objects.all()
    return render(request, 'scoreboard/scoreboard.html', {'games': games})


@login_required
def redemption_view(request):
    try:
        current_user_player = request.user.player
    except Player.DoesNotExist:
        current_user_player = None

    if not current_user_player:
        messages.error(request, 'Your are not a registered Player!')
        return redirect('/gfp-system')

    if request.method == 'POST':
        form = PointCodeForm(request.POST)
        if form.is_valid():
            point_code = PointCode.objects.filter(code=form.cleaned_data['code'], consumed_on=None)
            if point_code.exists():
                code = point_code[0]
                code.consume_code(current_user_player)
                messages.info(request, 'You have gained {points} points!'.format(points=code.score))
            else:
                messages.error(request, 'Invalid code provided!')
        else:
            messages.error(request, 'Invalid code provided!')
    else:
        form = PointCodeForm()

    return render(request, 'scoreboard/pointcode.html', {'form': form})


@login_required
def guess_view(request, id):
    associated_game_session = get_object_or_404(GameSession, pk=id)
    form = GuessingForm()
    if associated_game_session.game.game_type != Game.GUESSING:
        return HttpResponseForbidden()

    game_name = associated_game_session.game.name
    if request.method == 'POST':
        try:
            current_user_player = request.user.player
        except Player.DoesNotExist:
            current_user_player = None
        if current_user_player:
            guess_object, created = Guess.objects.get_or_create(player=current_user_player,
                                                                game_session=associated_game_session)
            form = GuessingForm(request.POST, instance=guess_object)
            if form.is_valid():
                new_guess = form.save()
                messages.info(request, 'Your guess has been successfully recorded!')
            else:
                messages.error(request, 'Something went wrong!')
        else:
            messages.warning(request, 'You are most likely a cheeky admin!')
    return render(request, 'scoreboard/guesser.html', {'form': form,
                                                       'game': game_name})
