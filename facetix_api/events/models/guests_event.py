"""Invitados al Evento model."""

# Django
from django.db import models

# Models
from facetix_api.utils.models.base import DateBaseModel


class GuestEvent(DateBaseModel):

    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    guest = models.ForeignKey('events.Guest', on_delete=models.RESTRICT)

    def __str__(self):
        return "GuestEvent id: {} event: {} ".format(
            self.id, self.event)
    
    class Meta:
        db_table = 'guests_events'
        managed = True
        verbose_name = 'Guest Event'
        verbose_name_plural = 'Guests Events'
