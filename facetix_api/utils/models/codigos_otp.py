""" Verificación OTP Model """

# Django
from django.db import models
from django.core.validators import RegexValidator

from datetime import datetime

from facetix_api.utils.models.base import DateBaseModel


class CodigoOtp(DateBaseModel):

    class EstadosChoices(models.TextChoices):
        ACTIVO = 'ACTIVO'
        INACTIVO = 'VENCIDO'
        VALIDADO = 'EXITOSO'
        INVALIDO = 'INVALIDO'

    email = models.EmailField()
    codigo = models.CharField(max_length=6)
    fecha_vigencia = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_ultimo_envio = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    estado = models.CharField(
        max_length=10,
        choices=EstadosChoices.choices,
        default=EstadosChoices.ACTIVO
    )
    conteo_intentos = models.SmallIntegerField(default=0)
    maximo_intentos = models.SmallIntegerField(default=1)

    def __str__(self):
        return "CodigoOtp id: {} email: {} estado: {}".format(self.id, self.email, self.estado)

    class Meta(DateBaseModel.Meta):
        db_table = 'codigo_otp'
        managed = True
        verbose_name = 'verificacion_otp'
        verbose_name_plural = 'verificaciones_otp'

    def inactivar_registro(self):
        self.estado = CodigoOtp.EstadosChoices.INACTIVO
        self.updated_at = datetime.now()
        self.save()

    def is_registro_vigente(self):
        tiempo = (self.fecha_vigencia - datetime.now())
        if tiempo.total_seconds() > 0:
            return True
        return False

    def get_segundos_desde_ultimo_envio(self):
        tiempo = (datetime.now() - self.fecha_ultimo_envio)
        return tiempo.total_seconds()


class ConfiguracionCodigoOtp(DateBaseModel):
    maximo_intentos = models.SmallIntegerField()
    tiempo_bloqueo_usuario = models.SmallIntegerField()

    def __str__(self):
        return "ConfiguracionCodigoOtp id: {} maximo_intentos: {} tiempo_bloqueo_usuario: {} ".format(
            self.id, self.maximo_intentos, self.tiempo_bloqueo_usuario)

    class Meta(DateBaseModel.Meta):
        db_table = 'configuracion_codigo_otp'
        managed = True
        verbose_name = 'configuracion_codigo_otp'
        verbose_name_plural = 'configuracion_codigo_otp'
