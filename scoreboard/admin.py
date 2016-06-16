from django.contrib import admin
from django.db.models import Q, F
from .models import Game, Score, GameSession, GamePrize, AggregatedScore, PartialScore, SingleScore, PointCode
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from games.models import Guess

class SingleScoreInline(admin.TabularInline):
    model = SingleScore

    # Allow superuser to add score
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(SingleScoreInline, self).get_readonly_fields(request, obj)
        else:
            return ('score', )

class AggregatedScoreInline(admin.TabularInline):
    model = AggregatedScore
    fields = ('player', 'average_score', 'score', 'view_breakdown' )
    readonly_fields = ('average_score', 'score', 'view_breakdown' )

    def view_breakdown(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        url = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(instance.id,))
        if instance.id:
            uri = '<a href="%s">View Breakdown</a>' % (url,)
            return mark_safe(uri)
        else:
            return '-'

class GameSessionInline(admin.TabularInline):
    model = GameSession
    readonly_fields = ('total_participants', )

    def total_participants(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        url = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=(instance.id,))
        score = instance.score_set.count()
        if instance.id:
            uri = '<a href="%s">%s</a>' % (url, score)
        else:
            uri = score
        return mark_safe(uri)

    total_participants.allow_tags = True

class GuessInline(admin.TabularInline):
    model = Guess
    field = ('player', 'guess', 'closeness', )
    readonly_fields = ('closeness', )

    def closeness(self, instance):
        if instance.id is None:
            return '-'
        actual_value = instance.game_session.guess_value
        return '%d' % (abs(instance.guess - actual_value))

class GuessAdmin(admin.ModelAdmin):
    model = Guess

class PartialScoreInline(admin.TabularInline):
    model = PartialScore

class AggregatedScoreAdmin(admin.ModelAdmin):
    model = AggregatedScore
    inlines = [
        PartialScoreInline,
    ]

    list_display = ('player', 'game', 'score')
    readonly_fields = ('score', )

class GameSessionAdmin(admin.ModelAdmin):

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        inlines = []
        if obj is None:
            return []

        if obj.game.game_type == obj.game.JUDGE:
            inlines.append(AggregatedScoreInline)
        else:
            inlines.append(SingleScoreInline)

        if obj.game.game_type == obj.game.GUESSING:
            inlines.append(GuessInline)

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)

        return inline_instances

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
        if formset.model == SingleScore:
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
        else:
            if formset.is_valid():
                formset.save()

class GamePrizeInline(admin.TabularInline):
    model = GamePrize

class GameAdmin(admin.ModelAdmin):
    inlines = [
        GamePrizeInline,
        GameSessionInline,
    ]

class PointCodeAdmin(admin.ModelAdmin):
    model = PointCode

admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(AggregatedScore, AggregatedScoreAdmin)
admin.site.register(Guess, GuessAdmin)
admin.site.register(PointCode, PointCodeAdmin)
