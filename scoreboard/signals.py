from django.db.models import F, Func
from django.db.models.signals import post_save
from django.dispatch import receiver
from scoreboard.models import PartialScore, GameSession, Game

import math


def get_sorted_guesses(instance):
    all_guesses = instance.guess_set.all()
    correct_value = instance.game.guess_value
    annotated_guesses = all_guesses.annotate(difference=Func(F('guess') - correct_value, function='ABS'))
    sorted_guesses = annotated_guesses.order_by('guess', '-guessed_on')

    return sorted_guesses

@receiver(post_save, sender=GameSession, dispatch_uid="tally_guessing_scores")
def tally_guessing_scores(sender, instance, **kwargs):
    """
    Commit scores to DB for Guessing-type games.
    """
    if instance.is_active or instance.game.game_type != Game.GUESSING or not instance.guess_set.count():
        return

    sorted_guesses = get_sorted_guesses(instance)



@receiver(post_save, sender=PartialScore, dispatch_uid="update_total_score")
def update_total_score(sender, instance, **kwargs):
    all_partial_scores = instance.aggregated_score.partialscore_set.all()
    calculated_score = 0

    for partial_score in all_partial_scores:
        calculated_score += partial_score.percentage/100 * partial_score.score

    instance.aggregated_score.score = math.floor(calculated_score)
    instance.aggregated_score.save()
