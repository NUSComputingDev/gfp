from django.db import models

from players.models import Player
from scoreboard.models import GameSession


class Guess(models.Model):
    """
    Guess model - tracks down users guesses for a particular GameSession
    """
    player = models.ForeignKey(Player)
    game_sesion = models.ForeignKey(GameSession)
    guess = models.PositiveIntegerField()
    guessed_on = models.DateField(auto_now=True)