# admin.py
from django.contrib import admin
from .models import PopupEvent, PopupClick

@admin.register(PopupEvent)
class PopupEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    actions = ['make_active']

    def make_active(self, request, queryset):
        PopupEvent.objects.update(is_active=False)
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected popups as active"

@admin.register(PopupClick)
class PopupClickAdmin(admin.ModelAdmin):
    list_display = ('event', 'ip_address', 'clicked_at')
