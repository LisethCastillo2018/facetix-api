from django.contrib import admin

from facetix_api.events.models import TypeEvent, Guest, GuestEvent, Event


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('pk',)
    list_display = ('name', 'created', 'updated')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('pk',)
    list_display = ('name', 'guest_type', 'created', 'updated')


@admin.register(GuestEvent)
class GuestEventAdmin(admin.ModelAdmin):
    search_fields = ('event',)
    ordering = ('pk',)
    list_display = ('event', 'guest', 'created', 'updated')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('pk',)
    list_display = ('name', 'date', 'time', 'place', 'address', 'organizer', 'event_type', 'is_active', 'created', 'updated')