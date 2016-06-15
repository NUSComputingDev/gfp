from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from players.models import Player
from scoreboard.models import GameSession


class Guess(models.Model):
    """
    Guess model - tracks down users guesses for a particular GameSession
    """
    player = models.ForeignKey(Player)
    game_session = models.ForeignKey(GameSession)
    guess = models.PositiveIntegerField()
    guessed_on = models.DateField(auto_now=True)

    def save(self, **kwargs):
        if not self.game_session.is_active:
            return
        else:
            super(Guess, self).save(**kwargs)
