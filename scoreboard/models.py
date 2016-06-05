from django.db import models
from django.db.models import Q
from django.conf import settings

# Model for Games
class Game(models.Model):
    NORMAL = 'NM'
    GUESSING = 'GS'
    JUDGE = 'JD'
    GAME_TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (GUESSING, 'Guessing'),
        (JUDGE, 'Judge')
    )
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=NORMAL
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    def __str__(self):
        return '%s' % (self.name)

# Represents a Game Session for a Game!
class GameSession(models.Model):
    game_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    guess_value = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s #%d' % (self.game, self.id)

# Represents a Game Session with aggregate Scoring
class AggregateGameSession(GameSession):
    players = models.ManyToManyField('players.Player')

# Scoring for a particular rank in game_master
class GamePrize(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)
    score = models.IntegerField(default=0)

    def __str__(self):
        return '%d' % (self.rank)

    class Meta:
        unique_together = ("game", "rank")

# Abstract base model for Scoring
class AbstractScore(models.Model):
    game_session = models.ForeignKey('GameSession', on_delete=models.CASCADE)
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "%s's score for %s" % (self.player, self.game_session.game)

    class Meta:
        abstract = True

# Score for a GameSession
class Score(AbstractScore):
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ("game_session", "position")
        ordering = ['position']

class AggregatedScore(AbstractScore):
    def game(self):
        return self.game_session.game

    def player_name(self):
        return self.player

    def average_score(self):
        cumulative_score = self.total_score()
        judges_count = self.partialscore_set.count()
        if judges_count == 0:
            return 0
        return cumulative_score / judges_count

    def total_score(self):
        partial_scores = self.partialscore_set.all()
        cumulative_score = 0

        for partial in partial_scores:
            cumulative_score += partial.score * (partial.percentage / 100)

        return cumulative_score

# Score for an aggregated GameSession
class PartialScore(models.Model):
    aggregated_score = models.ForeignKey('AggregatedScore', on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(default=0)
    game_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.aggregated_score)

    class Meta:
        ordering = ['-percentage']
        unique_together = ("aggregated_score", "game_master")

class Guess(models.Model):
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    guess = models.PositiveIntegerField(default=0)
    game_session = models.ForeignKey('GameSession',
                                     on_delete=models.CASCADE,
                                     limit_choices_to=Q(game__game_type=Game.GUESSING))

    def __str__(self):
        return '%s: %d' % (self.player, self.guess)

    class Meta:
        unique_together = ("game_session", "player")
        verbose_name_plural = 'Guesses'