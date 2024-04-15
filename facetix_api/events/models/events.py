"""Invitados model."""

# Django
from django.db import models

# Models
from facetix_api.utils.models.base import DateBaseModel


def directory_path(instance, filename):
    return 'files/events/{0}/{1}'.format(instance.date, filename)


class EventManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)
    

class Event(DateBaseModel):

    name = models.TextField(max_length=150, verbose_name='Name')
    date = models.DateField(
        'Event Date', help_text='Date the event will take place.'
    )
    time = models.TimeField(
        'Event Time', help_text='Time the event will take place.'
    )
    place = models.TextField(max_length=250, verbose_name='Place')
    address = models.TextField(max_length=150, verbose_name='Address')
    city = models.ForeignKey('utils.City', on_delete=models.RESTRICT)
    organizer = models.ForeignKey('users.User', on_delete=models.RESTRICT)
    event_type = models.ForeignKey('events.TypeEvent', on_delete=models.RESTRICT)
    description = models.TextField(max_length=150, verbose_name='Description', blank=True)
    capacity = models.IntegerField()
    file_cover = models.FileField(upload_to=directory_path, null=True)
    is_active = models.BooleanField(default=True)

    objects = EventManager()

    def __str__(self):
        return "Event id: {} name: {} ".format(
            self.id, self.name)
    
    class Meta:
        db_table = 'event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
