from django.contrib import admin
from .models import Game, Score, GameSession, GamePrize
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

class ScoreInline(admin.TabularInline):
    model = Score
    exclude = ('score', )

class GameSessionInline(admin.TabularInline):
    model = GameSession
    readonly_fields = ('total_participants', )

    def total_participants(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        url = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(instance.id,))
        uri = '<a href="%s">%s</a>' % (url, instance.score_set.count())
        return mark_safe(uri)

    total_participants.allow_tags = True

class GameSessionAdmin(admin.ModelAdmin):
    inlines = [
        ScoreInline,
    ]

class GamePrizeInline(admin.TabularInline):
    model = GamePrize

class GameAdmin(admin.ModelAdmin):
    inlines = [
        GamePrizeInline,
        GameSessionInline,
    ]

admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
