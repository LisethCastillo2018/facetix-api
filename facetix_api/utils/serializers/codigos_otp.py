
# Django REST Framework
from rest_framework import serializers

from facetix_api.utils.models.codigos_otp import CodigoOtp

class CodigoOtpModelSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class."""
        model = CodigoOtp
        fields = ('id', 'email', 'estado', 'fecha_vigencia', 'created', 'updated')
