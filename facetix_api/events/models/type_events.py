"""Tipo de Eventos model."""

# Django
from django.db import models
# Models
from facetix_api.utils.models.base import DateBaseModel


class TypeEvent(DateBaseModel):
    name = models.TextField(max_length=150, verbose_name='Name', blank=True)

    def __str__(self):
        return "TypeEvent id: {} name: {} ".format(
            self.id, self.name)
    
    class Meta:
        db_table = 'type_events'
        managed = True
        verbose_name = 'Type Event'
        verbose_name_plural = 'Type Events'
