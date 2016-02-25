from django.contrib import admin
from .models import Game, Score

class ScoreInline(admin.TabularInline):
    model = Score

class GameAdmin(admin.ModelAdmin):
    inlines = [
        ScoreInline,
    ]

admin.site.register(Game, GameAdmin)
