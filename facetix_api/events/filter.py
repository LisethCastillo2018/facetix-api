
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

# Models
from .models.events import Event


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class EventFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    events_type = NumberInFilter(field_name='event_type', lookup_expr='in')

    class Meta:
        model = Event
        fields = [
            'created__gte', 'created__lte', 'events_type', 'is_active'
        ]