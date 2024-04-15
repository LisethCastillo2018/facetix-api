"""
Se usa el patrón de clase abstracta, para evitar la repetición de código, centralizando las funcionalidades
comunes en una clase que sirve de plantilla para las clases hijas.
Tener en cuenta que esta clase no puede ser instanciada directamente.
"""

import math
import random
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from facetix_api.users.models.users import BloquedUser, User

from facetix_api.utils.models.codigos_otp import CodigoOtp, ConfiguracionCodigoOtp


class CodigoOtpLogicClass:

    LONGITUD_CODIGO = 6
    MINUTOS_VIGENCIA = 15
    SEGUNDOS_MINIMOS_PARA_REENVIO = 60

    def __init__(self, email, codigo=None):
        self.email = email
        self.codigo = codigo
        self.object_otp = None

    def enviar_email(self, title, template):
        """
        Permite enviar un código OTP vigente o nuevo vía E-mail a un email determinado.
        Se retorna ok=True si se ha generado un código correctamente y se ha enviado via E-mail al
        número de email dado. En cambio, se retorna ok=False si el tiempo transcurrido desde
        el ultimo envío al numero de ceular es menor a 1 minuto
        """

        if self.object_otp is not None:
            object_otp = self.object_otp
        else:
            object_otp = self._get_registro_activo()

        is_vigente = (False if object_otp is None else object_otp.is_registro_vigente())

        if is_vigente:
            # Si el total de segundos desde el ultimo envio es menor a 60, no se realiza el envío
            seg_ultimo_envio = object_otp.get_segundos_desde_ultimo_envio()
            if seg_ultimo_envio < self.SEGUNDOS_MINIMOS_PARA_REENVIO:
                return {
                    'ok': False,
                    'message': 'El tiempo transcurrido desde el último envío es menor a {} segundos'.format(
                        self.SEGUNDOS_MINIMOS_PARA_REENVIO
                    ),
                    'data_error': {
                        'segundos_minimos_para_reenvio': self.SEGUNDOS_MINIMOS_PARA_REENVIO,
                        'segundos_transcurridos': round(seg_ultimo_envio),
                        'segundos_restantes': (self.SEGUNDOS_MINIMOS_PARA_REENVIO - round(seg_ultimo_envio)),
                    },
                    'data': None
                }
        else:

            if object_otp is not None:
                # Inactivar registro caducado
                object_otp.inactivar_registro()

            # Crear nuevo registro vigente y activo
            object_otp = self._crear_registro()

        # enviar mensaje
        self._envio_email(object_otp.codigo, title, template)

        # actualizar fecha ultimo envio
        object_otp.fecha_ultimo_envio = datetime.now()
        object_otp.save()

        return {'ok': True, 'data': object_otp}

   
    def reenviar_email(self, title, template):
        """
        Permite reenviar un código OTP vigente o nuevo vía E-mail a un email determinado.

        Funciona igual que enviar_email. Adicionalmente, para esta opción debe existir un primer envio
        o registro activo, si se trata de un registro activo y vigente, se renovara su fecha de vigencia.
        """

        self.object_otp = self._get_registro_activo()

        # Cuando es un reenvio se valida que exista un registro activo
        if self.object_otp is None:
            return {
                'ok': False,
                'message': 'No existe un envío activo.',
                'data': None
            }

        resultado = self.enviar_email(title, template)

        if resultado['ok'] is True:
            # Cuando es reenvio se renueva la vigencia del registro
            object_otp = resultado['data']
            object_otp.fecha_vigencia = self._get_fecha_vigencia()
            object_otp.save()
            resultado['data'] = object_otp

        return resultado

    def validar_codigo_email(self):
        """
        Permite validar un código para un número de email.

        Se retorna ok=True si el código es correcto para validar el email, de lo contrario
        se retorna ok=False y un mensaje respectivo
        """

        object_otp = self._get_registro_activo()
        is_vigente = (False if object_otp is None else object_otp.is_registro_vigente())

        if object_otp is None:
            return {
                'ok': False,
                'message': 'No existe un código pendiente de validación.',
                'data': None
            }
        
        if str(object_otp.codigo).strip() != str(self.codigo).strip():

            object_otp.conteo_intentos = object_otp.conteo_intentos + 1 
            object_otp.save()

            if object_otp.conteo_intentos == object_otp.maximo_intentos:
                user_obj = User.objects.get(email=self.email)
                configuracion_otp = ConfiguracionCodigoOtp.objects.first()
                tiempo_bloqueo = configuracion_otp.tiempo_bloqueo_usuario if configuracion_otp else 30
                
                BloquedUser.objects.create(
                    user=user_obj,
                    fecha_vigencia_bloqueo=(datetime.now() + timedelta(minutes=tiempo_bloqueo)),
                    observacion='Código OTP inválido. Excedió el número de intentos.´'
                )

                object_otp.estado = CodigoOtp.EstadosChoices.INVALIDO
                object_otp.fecha_vigencia = datetime.now()
                object_otp.updated_at = datetime.now()
                object_otp.save()

                return {
                    'ok': False,
                    'message': 'Código inválido. Excedió el número de intentos, su '
                               f'usuario ha sido bloqueado por {tiempo_bloqueo} minutos.',
                    'data': None
                }

            elif (object_otp.conteo_intentos + 1) == object_otp.maximo_intentos:
                return {
                    'ok': False,
                    'message': 'Código inválido, solo le queda un intento más. Verifique el código enviado '
                                'a su email y pruebe ingresandolo de nuevo.',
                    'data': None
                }
            
            return {
                    'ok': False,
                    'message': 'Código inválido. Verifique el código enviado '
                               'a su email y pruebe ingresandolo de nuevo.',
                    'data': None
                }
        
        else:
            if not is_vigente:
                return {
                    'ok': False,
                    'message': 'Código caducado. Pruebe reenviado un nuevo código a su email.',
                    'data': None
                }
     
            object_otp.estado = CodigoOtp.EstadosChoices.VALIDADO
            object_otp.fecha_vigencia = datetime.now()
            object_otp.updated_at = datetime.now()
            object_otp.save()

            return {'ok': True, 'data': object_otp}

    def verificar_codigo_email(self):
        """
        Permite verificar si un códgo y email han sido validados.

        Se retorna ok=True si el código se ha validado. En cambio, si el código para el número de email
        está en estado activo o inactivo, o no existe, se retorna ok=False.
        El código http que se retorna es 400.
        """

        object_otp = self._get_registro(email=self.email, codigo=self.codigo)
        if object_otp is None:
            return {
                'ok': False,
                'message': 'Código o email incorrectos',
                'data': None
            }
        elif object_otp.estado == CodigoOtp.EstadosChoices.VALIDADO:
            return {
                'ok': True,
                'data': object_otp
            }
        else:
            return {
                'ok': False,
                'message': 'El código no ha sido validado.',
                'data': object_otp
            }

    def _get_codigo(self):
        string = '0123456789'
        codigo_otp = ""
        length = len(string)
        for i in range(self.LONGITUD_CODIGO):
            codigo_otp += string[math.floor(random.random() * length)]
        return codigo_otp

    def _crear_registro(self):
        codigo_otp = self._get_codigo()
        configuracion_otp = ConfiguracionCodigoOtp.objects.first()
        datos = {
            'email': self.email,
            'codigo': codigo_otp,
            'fecha_vigencia': self._get_fecha_vigencia(),
            'conteo_intentos': 0,
            'maximo_intentos': configuracion_otp.maximo_intentos if configuracion_otp else 1
        }
        return CodigoOtp.objects.create(**datos)

    def _envio_email(self, codigo, title, template):
        # send an e-mail 
        context = {
            'codigo': codigo,
        }

        # render email text
        email_html_message = render_to_string(template, context)

        msg = EmailMultiAlternatives(
            # title:
            title,
            # message:
            "",
            # from:
            settings.EMAIL_FROM,
            # to:
            [self.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

    def _get_registro(self, email, codigo=None, estado=None):

        filtros = {'email': email}

        if estado is not None:
            filtros['estado'] = estado

        if codigo is not None:
            filtros['codigo'] = codigo

        qs = CodigoOtp.objects.filter(**filtros).order_by('-fecha_vigencia')
        return qs.first()

    def _get_registro_activo(self):

        return self._get_registro(
            email=self.email,
            estado=CodigoOtp.EstadosChoices.ACTIVO
        )

    def _get_fecha_vigencia(self):
        return (datetime.now() + timedelta(minutes=self.MINUTOS_VIGENCIA))
