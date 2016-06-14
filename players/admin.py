from django.contrib import admin
from django.db.models import Q, F, Sum
from django.db.models.expressions import RawSQL
from .models import Player
from scoreboard.models import AggregatedScore, Score

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total_points')
    readonly_fields = ('total_points', )

    def get_queryset(self, request):
        qs = super(PlayerAdmin, self).get_queryset(request)
        qs = annotate_sum(qs, Score, 'score', 'total_points')
        return qs

    def total_points(self, instance):
        return instance.total_points

    total_points.admin_order_field = 'total_points'

def annotate_sum(qs, related_modelclass, field_name, annotation_name):
        raw_query = """
          SELECT COALESCE(SUM({field}), 0) FROM {model} AS model
            WHERE model.player_id = players_player.id
        """.format(
            field = field_name,
            model = related_modelclass._meta.db_table,
        )

        annotation = {annotation_name: RawSQL(raw_query, [])}
        return qs.annotate(**annotation)