from django.contrib import admin

from games.models import RaffleTicket, Draw


@admin.register(RaffleTicket)
class RaffleTicketAdmin(admin.ModelAdmin):
    model = RaffleTicket

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    model = Draw
    list_display = ('game', 'winner', 'draw_on')
    readonly_fields = ('draw_on', )

class DrawInlineAdmin(admin.TabularInline):
    model = Draw
    readonly_fields = ('draw_on',)

