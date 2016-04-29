from django.contrib import admin
from django.db.models import Q
from .models import Player
from scoreboard.models import Score

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total_points', )
    readonly_fields = ('total_points', )

    def total_points(self, instance):
        total = 0
        games = Score.objects.filter(player=instance)
        for game in games:
            total += game.score
        return total