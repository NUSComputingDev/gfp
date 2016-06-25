from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from players.models import Player
from scoreboard.models import GameSession, Game


class Guess(models.Model):
    """
    Guess model - tracks down users guesses for a particular GameSession
    """
    player = models.ForeignKey(Player)
    game_session = models.ForeignKey(GameSession)
    guess = models.PositiveIntegerField(default=0)
    guessed_on = models.DateField(auto_now=True)

    def save(self, **kwargs):
        if not self.game_session.is_active:
            return
        else:
            super(Guess, self).save(**kwargs)


class Draw(models.Model):
    """
    Representation of a Draw - where a winner is selected from a pool
    """
    game = models.ForeignKey(Game)
    draw_on = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(Player, blank=True, null=True)

    def save(self, **kwargs):
        if self.winner:
            RaffleTicket.objects.filter(player=self.winner).delete()
        super(Draw, self).save(**kwargs)


class RaffleTicket(models.Model):
    """
    Raffle ticket - used in games that are based on luck
    """
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game, limit_choices_to={'game_type': Game.LUCKY_DRAW})

    def __str__(self):
        return '{player}\'s entry for {raffle}'.format(player=self.player, raffle=self.game)
