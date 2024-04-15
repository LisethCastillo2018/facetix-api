"""Archivos multimedia del evento model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from facetix_api.utils.models.base import DateBaseModel


def directory_path(instance, filename):
    return 'files/events/{0}/{1}'.format(instance.event.id, filename)


class EventMediaManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)
    

class EventMedia(DateBaseModel):

    class TypeChoices(models.TextChoices):
        GALLERY = 1, _('GALLERY')
        COVER = 2, _('COVER')

    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    file = models.FileField(
        null=True,
        upload_to=directory_path,
    )
    type = models.CharField(
        choices=TypeChoices.choices,
        default=TypeChoices.GALLERY,
        max_length=1,
    )
    is_active = models.BooleanField(default=True)

    objects = EventMediaManager()

    def __str__(self):
        return "EventMedia id: {} event: {} ".format(
            self.id, self.event)
    
    class Meta:
        db_table = 'events_media'
        managed = True
        verbose_name = 'Event Media'
        verbose_name_plural = 'Event Media'
