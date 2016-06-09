from django.contrib import admin
from django.db.models import Q, F, Sum
from django.db.models.expressions import RawSQL
from .models import Player
from scoreboard.models import AggregatedScore, Score

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'normal_points', 'aggregated_points', 'total_points', )
    readonly_fields = ('normal_points', 'aggregated_points', 'total_points', )

    def get_queryset(self, request):
        qs = super(PlayerAdmin, self).get_queryset(request)
        qs = annotate_sum(qs, AggregatedScore, 'score', 'aggregated_points')
        qs = annotate_sum(qs, Score, 'score', 'normal_points')
        qs = qs.annotate(total_points=F('aggregated_points') + F('normal_points'))
        return qs

    def normal_points(self, instance):
        return instance.normal_points

    def aggregated_points(self, instance):
        return instance.aggregated_points

    def total_points(self, instance):
        return instance.total_points

    total_points.admin_order_field = 'total_points'
    aggregated_points.admin_order_field  = 'aggregated_points'
    normal_points.admin_order_field = 'normal_points'

def annotate_sum(qs, related_modelclass, field_name, annotation_name):
        raw_query = """
          SELECT SUM({field}) FROM {model} AS model
            WHERE model.player_id = players_player.id
        """.format(
            field = field_name,
            model = related_modelclass._meta.db_table,
        )

        annotation = {annotation_name: RawSQL(raw_query, [])}
        return qs.annotate(**annotation)