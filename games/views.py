import random

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from games.models import RaffleTicket, Draw
from scoreboard.models import Game


@user_passes_test(lambda u: u.is_superuser)
def draw_view(request, game_id):
    game = Game.objects.get(id=game_id)
    if game.game_type != Game.LUCKY_DRAW:
        return redirect('players:players-login')
    print(request.POST)
    if request.POST and request.POST.get('start_draw'):
        entries = RaffleTicket.objects.filter(game_id=game_id)
        entry_count = entries.count()
        if entry_count == 0:
            return redirect('players:players-login')
        random_idx = random.randint(0, entry_count - 1)

        draw = Draw.objects.create(game_id=game_id, winner=entries[random_idx].player)

        return render(request, 'games/draw_result.html', {'draw': draw})

    return render(request, 'games/draw_button.html')

