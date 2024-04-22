"""Events serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from facetix_api.events.models import Event
from facetix_api.events.models.events_media import EventMedia
from facetix_api.events.serializers.events_media import EventMediaModelSerializer

# Serializers
from facetix_api.users.models.users import User
from facetix_api.utils.serializers.globals import DataSerializer
from facetix_api.users.serializers.users import UserModelSerializer


class EventModelSerializer(serializers.ModelSerializer):
    city = DataSerializer()
    organizer = UserModelSerializer()
    event_type = DataSerializer()

    class Meta:
        model = Event
        fields = '__all__'


class UpdateAndCreateEventSerializer(serializers.ModelSerializer):
    """
    Update and create event serializer.
    """
    file_cover = serializers.FileField(required=True)

    class Meta:
        """Meta class."""
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        validated_data["is_active"] = True
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ValidateUserEntrySerializer(serializers.Serializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user_photo = serializers.FileField()