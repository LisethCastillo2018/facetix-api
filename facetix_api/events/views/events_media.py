"""Views event."""
# Django
from django.utils.decorators import method_decorator
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Models
from facetix_api.events.models import EventMedia

# Serializers
from facetix_api.events import serializers

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# from facetix_api.events.filter import EventMediaFilter


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class EventMediaViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API de eventos
    """

    queryset = EventMedia.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    # filterset_class = EventMediaFilter

    def get_serializer_class(self):
        return serializers.EventMediaModelSerializer

    def get_permissions(self):
        # if self.action in ['login', 'password_reset', 'confirm_password_reset']:
        #     """ Cuando en 'Login' no se solicita al evento estar autenticado """
        #     permissions = [AllowAny]
        # else:
        #     permissions = [IsAuthenticated]
        permissions = [AllowAny]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ Listar archivos multimedia de eventos

            Permite listar todos los archivos multimedia de eventos registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar archivos multimedia de evento por ID

            Permite obtener información de un archivos multimedia de evento dado su ID
        """
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear archivos multimedia de eventos

            Permite crear archivos multimedia de eventos
        """
        serializer = serializers.UpdateAndCreateEventMediaSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Actualizar archivos multimedia de eventos
        
            Perimite la actualización de un archivos multimedia de evento dado su ID.
        """
        event = self.get_object()
        serializer = serializers.UpdateAndCreateEventMediaSerializer(
            instance=event,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Disable fole multimedia event."""
        instance.is_active = False
        instance.save()
