"""Events serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from facetix_api.events.models import BuyEventTicket

# Serializers
from facetix_api.utils.serializers.globals import DataChoiceSerializer
from facetix_api.users.serializers.users import UserModelSerializer
from facetix_api.events.serializers.events import EventModelSerializer


class BuyEventTicketModelSerializer(serializers.ModelSerializer):
    category = DataChoiceSerializer()
    assistant = UserModelSerializer()
    event = EventModelSerializer()

    class Meta:
        model = BuyEventTicket
        fields = '__all__'


class UpdateAndCreateBuyEventTicketSerializer(serializers.ModelSerializer):
    """
    Update and create event serializer.
    """

    total_cost = serializers.FloatField(required=False)

    def validate(self, data):
        data['total_cost'] = data['cost'] * data['number']
        return data

    class Meta:
        """Meta class."""
        model = BuyEventTicket
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
