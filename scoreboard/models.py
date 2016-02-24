from django.db import models

# Model for Games that are played
class Game(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()

# Score for the Game
class Score(models.Model):
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
