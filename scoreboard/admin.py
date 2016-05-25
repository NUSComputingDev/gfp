from django.contrib import admin
from django.db.models import Q
from .models import Game, Score, GameSession, GamePrize
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

class ScoreInline(admin.TabularInline):
    model = Score

    # Allow superuser to add score
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ScoreInline, self).get_readonly_fields(request, obj)
        else:
            return ('score', )

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

    def get_readonly_fields(self, request, obj=None):
        base_readonly = super(GameSessionAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            base_readonly = base_readonly + ('game_master', )
        return base_readonly

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.game_master = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Score:
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for instance in instances:
                q = GamePrize.objects.filter(Q(rank=instance.position) & Q(game=instance.game_session.game))
                if q.exists():
                    # Prevent tampering of score for non-superusers
                    if instance.score <= 0 or not request.user.is_superuser:
                        instance.score = q[0].score
                instance.save()
            formset.save_m2m()

class GamePrizeInline(admin.TabularInline):
    model = GamePrize

class GameAdmin(admin.ModelAdmin):
    inlines = [
        GamePrizeInline,
        GameSessionInline,
    ]

admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
