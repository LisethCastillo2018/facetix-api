"""Costo de tiquetes del evento model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from facetix_api.utils.models.base import DateBaseModel


class EventTicketCost(DateBaseModel):

    class CategoryChoices(models.TextChoices):
        GENERAL = 1, _('GENERAL')
        VIP = 2, _('VIP')

    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    cost = models.FloatField()
    category = models.CharField(
        choices=CategoryChoices.choices,
        default=CategoryChoices.GENERAL,
        max_length=1,
    )

    def __str__(self):
        return "EventTicketCost id: {} event: {} ".format(
            self.id, self.event)
    
    class Meta:
        db_table = 'events_ticket_cost'
        managed = True
        verbose_name = 'Event Ticket Cost'
        verbose_name_plural = 'Event Ticket Cost'
