"""Invitados model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from facetix_api.utils.models.base import DateBaseModel

class Guest(DateBaseModel):

    class GuestTypeChoices(models.TextChoices):
        EXPOCITOR = 1, _('EXPOCITOR')
        ARTISTA = 2, _('ARTISTA')
        DEPORTISTA = 3, _('DEPORTISTA')

    name = models.TextField(max_length=150, verbose_name='Name', blank=True)
    guest_type = models.CharField(
        choices=GuestTypeChoices.choices,
        default=GuestTypeChoices.ARTISTA,
        max_length=1, null=True, blank=True
    )

    def __str__(self):
        return "Guest id: {} name: {} ".format(
            self.id, self.name)
    
    class Meta:
        db_table = 'guests'
        managed = True
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
