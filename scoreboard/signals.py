from django.db.models.signals import post_save
from django.dispatch import receiver
from scoreboard.models import PartialScore

import math


@receiver(post_save, sender=PartialScore, dispatch_uid="update_total_score")
def update_total_score(sender, instance, **kwargs):
    all_partial_scores = instance.aggregated_score.partialscore_set.all()
    calculated_score = 0

    for partial_score in all_partial_scores:
        calculated_score += partial_score.percentage/100 * partial_score.score

    instance.aggregated_score.score = math.floor(calculated_score)
    instance.aggregated_score.save()