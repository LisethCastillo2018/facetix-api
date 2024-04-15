"""Views user."""
# Django
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth import password_validation

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Models
from facetix_api.users.models import User

# Serializers
from facetix_api.users import serializers

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from facetix_api.users.filter import UsersFilter
from facetix_api.utils.logic.codigos_otp import CodigoOtpLogicClass
from facetix_api.utils.serializers.codigos_otp import CodigoOtpModelSerializer


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class UserViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API de usuarios
    """

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsersFilter

    def get_serializer_class(self):
        if self.action in ['login']:
            """ Cuando es 'login' se asigna un serializador dirente """
            return serializers.CustomTokenObtainPairSerializer
        return serializers.UserModelSerializer

    def get_permissions(self):
        # if self.action in ['login', 'password_reset', 'confirm_password_reset']:
        #     """ Cuando en 'Login' no se solicita al usuario estar autenticado """
        #     permissions = [AllowAny]
        # else:
        #     permissions = [IsAuthenticated]
        permissions = [AllowAny]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ Listar usuarios

            Permite listar todos los usuarios registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar usuario por ID

            Permite obtener información de un usuario dado su ID
        """
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear usuarios

            Permite crear usuarios, los cuales podrán logearse en el sistema.
        """
        print("*** datos recibidos del usuario: ", request.data)
        serializer = serializers.UpdateAndCreateUserSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = self.get_serializer(instance=user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Actualizar usuarios
        
            Perimite la actualización de un usuario dado su ID.
        """
        print("*** datos recibidos del usuario: ", request.data)
        user = self.get_object()
        serializer = serializers.UpdateAndCreateUserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = self.get_serializer(instance=user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Disable membership."""
        instance.is_active = False
        instance.save()

    @swagger_auto_schema(responses={200: serializers.UserLoginSerializer(many=False)})
    @action(detail=False, methods=['post'])
    def login(self, request):
        """ Autenticar usuarios.

            - Permite autenticar un usuario por medio de email y contraseña.
            - En caso de éxito, retorna la información del usuario y del token de acceso.
        """
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = serializers.UserLoginSerializer(instance={'user': user, 'token': token}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """ Inhabilitar token de acceso a usuarios.

            - Permite inhabilitar el token de acceso del usuario.
            - Este endpoint no retorna información.
        """
        serializer = serializers.RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def password_validations(self, request):
        """ Lista las validaciones de contraseña habilitadas. """
        data = password_validation.password_validators_help_texts()
        return Response(data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'])
    def password_reset(self, request):
        """ Enviar email para restablecer contraseña. """
        serializer = serializers.ValidateSendResetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            otp = CodigoOtpLogicClass(data['email'])
            result = otp.enviar_email(
                title="Tivkify App - Restablecer Contraseña", 
                template="email/user_reset_password.html"
            )
        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if result['data'] is not None:
            result['data'] = CodigoOtpModelSerializer(result['data']).data

        if not result['ok']:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['message'] = "Se ha enviado un código a la dirección de correo ingresada."
            return Response(result, status=status.HTTP_200_OK)
        
    @transaction.atomic
    @action(detail=False, methods=['post'])
    def confirm_password_reset(self,  request, *args, **kwargs):
        """ Confirma restablacimiento de contraseña. """
        serializer = serializers.ConfirmResetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            otp = CodigoOtpLogicClass(email=data['email'], codigo=data['codigo'])
            result = otp.validar_codigo_email()
        except Exception as error:
            return Response({'detail': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if result['data'] is not None:
            result['data'] = CodigoOtpModelSerializer(result['data']).data

        if not result['ok']:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Actualizar contraseña del usuario
            user = User.objects.get(email=data['email'])
            serializer = serializers.UpdateAndCreateUserSerializer(
                instance=user,
                data={'password': data['password']},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            result['message'] = "Contraseña restablecida exitosamente."
            return Response(result, status=status.HTTP_200_OK)
       