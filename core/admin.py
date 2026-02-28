from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, Event, Registration, Match

class EventAdmin(admin.ModelAdmin):
    # Added 'event_date' to the display and filter
    list_display = ('title', 'sub_category', 'event_date', 'entry_fee', 'winning_prize', 'status')
    list_filter = ('status', 'sub_category', 'event_date')
    search_fields = ('title', 'venue')
    ordering = ('event_date',) # Shows soonest events at the top by default

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'event', 'phone_number', 'payment_mode', 'is_paid', 'whatsapp_button')
    list_filter = ('event', 'payment_mode', 'is_paid')
    search_fields = ('player_name', 'pass_id', 'phone_number')

    # WHATSAPP LOGIC
    def whatsapp_button(self, obj):
        return format_html(
            '<a style="background-color:#25D366; color:white; padding:5px 10px; border-radius:5px; text-decoration:none; font-weight:bold;" '
            'href="https://wa.me/91{}?text=Hi {}, Welcome to Ueldo! Your pass for {} is confirmed." target="_blank">'
            '📱 WhatsApp</a>',
            obj.phone_number, obj.player_name, obj.event.title
        )
    whatsapp_button.short_description = "Marketing"

class MatchAdmin(admin.ModelAdmin):
    list_display = ('event', 'round_name', 'player_1', 'player_2', 'winner')
    list_filter = ('event', 'round_name')

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Match, MatchAdmin)