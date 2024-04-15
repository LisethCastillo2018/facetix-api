"""Events serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from facetix_api.events.models import EventMedia

# Serializers
from facetix_api.utils.serializers.globals import DataChoiceSerializer, DataSerializer
from facetix_api.users.serializers.users import UserModelSerializer


class EventMediaModelSerializer(serializers.ModelSerializer):
    type = DataChoiceSerializer()
    file = serializers.FileField(required=True)

    class Meta:
        model = EventMedia
        fields = '__all__'


class UpdateAndCreateEventMediaSerializer(serializers.ModelSerializer):
    """
    Update and create event serializer.
    """

    class Meta:
        """Meta class."""
        model = EventMedia
        fields = '__all__'

    def create(self, validated_data):
        validated_data["is_active"] = True
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
