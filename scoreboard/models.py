from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

import datetime


class Game(models.Model):
    """
    Model to represent a Game
    """
    NORMAL = 'NM'
    GUESSING = 'GS'
    JUDGE = 'JD'
    LUCKY_DRAW = 'LD'
    GAME_TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (GUESSING, 'Guessing'),
        (JUDGE, 'Judge'),
        (LUCKY_DRAW, 'Lucky Draw')
    )
    game_type = models.CharField(
        max_length=2,
        choices=GAME_TYPE_CHOICES,
        default=NORMAL
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    display_leaderboard = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.name)


class GameSession(models.Model):
    """
    Represents a game session for a Game
    """
    game_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    guess_value = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s #%d' % (self.game, self.id)


class GamePrize(models.Model):
    """
    Stores default scoring for a particular ranking in a game session
    """
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)
    score = models.IntegerField(default=0)

    def __str__(self):
        return '%d' % (self.rank)

    class Meta:
        unique_together = ("game", "rank")
        ordering = ['rank']


class Score(models.Model):
    """
    Base Model for Scoring
    """
    game_session = models.ForeignKey('GameSession', blank=True, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey('players.Player', blank=True, null=True, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return "%d point(s)" % (self.score)


class SingleScore(Score):
    """
    Classic scoring system: you get what you are given
    """
    position = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Checks for null-score and if there is, update it with the score from GamePrize.

        :param args:
        :param kwargs:
        :return:
        """
        if self.score is None:
            try:
                prize = GamePrize.objects.get(rank=self.position, game=self.game_session.game)
                self.score = prize.score
            except GamePrize.DoesNotExist:
                self.score = 0
            except MultipleObjectsReturned:
                self.score = 0

        super(SingleScore, self).save(*args, **kwargs)

    class Meta:
        ordering = ['position']


class AggregatedScore(Score):
    """
    Scoring system that is percentage based
    """

    def game(self):
        return self.game_session.game

    def average_score(self):
        cumulative_score = self.score
        judges_count = self.partialscore_set.count()
        if judges_count == 0:
            return 0
        return cumulative_score / judges_count


class PointCode(Score):
    """
    A 'scoring' system based on special predefined voucher-like codes
    """
    code = models.CharField(max_length=255)
    consumed_on = models.DateField(null=True, blank=True)

    def is_consumed(self):
        return self.consumed_on is not None

    def consume_code(self, player):
        self.player = player
        self.consumed_on = datetime.datetime.now()
        self.save()

    def __str__(self):
        return '%s' % (self.code)


# Score for an aggregated GameSession
class PartialScore(models.Model):
    """
    A score from a game master that contributes to the AggregatedScore
    """
    aggregated_score = models.ForeignKey('AggregatedScore', on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(default=0)
    game_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.aggregated_score)

    class Meta:
        ordering = ['-percentage']
        unique_together = ("aggregated_score", "game_master")
