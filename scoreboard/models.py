from django.db import models
from django.conf import settings

# Model for Games that are played
class Game(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    def __str__(self):
        return '%s' % (self.name)

# Represents a Game Session for a Game!
class GameSession(models.Model):
    game_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

# Scoring for a particular rank in game_master
class GamePrize(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ("game", "rank")

# Score for a GameSession
class Score(models.Model):
    game_session = models.ForeignKey('GameSession', on_delete=models.CASCADE)
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-score']
