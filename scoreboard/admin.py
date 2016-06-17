from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q, F, Func
from django import forms
from .models import Game, Score, GameSession, GamePrize, AggregatedScore, PartialScore, SingleScore
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from games.models import Guess


class SingleScoreInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(SingleScoreInlineFormset, self).clean()

        positions_used = []

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            else:
                if form.cleaned_data.get('DELETE', True):
                    continue

                data = form.cleaned_data
                pos = data.get('position')

                if pos is not None and pos in positions_used:
                    raise ValidationError(_('Position must be unique!'))

                positions_used.append(pos)

class SingleScoreInline(admin.TabularInline):
    model = SingleScore
    formset = SingleScoreInlineFormset

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

    def get_queryset(self, request):
        qs = super(GuessInline, self).get_queryset(request)
        return qs.annotate(closeness=Func(F('guess') - F('game_session__guess_value'), function='ABS'))\
                 .order_by('closeness')

    def closeness(self, instance):
        return instance.closeness

    closeness.admin_order_field = 'closeness'

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
        if formset.is_valid():
            if formset.model == SingleScore:
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                for instance in instances:
                    if not request.user.is_superuser:
                        instance.score = None
                    instance.save()
                formset.save_m2m()
            else:
                formset.save()

class GamePrizeInline(admin.TabularInline):
    model = GamePrize

class GameAdmin(admin.ModelAdmin):
    inlines = [
        GamePrizeInline,
        GameSessionInline,
    ]

admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(AggregatedScore, AggregatedScoreAdmin)
