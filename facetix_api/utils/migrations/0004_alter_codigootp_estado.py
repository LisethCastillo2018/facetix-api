# Generated by Django 4.2.6 on 2023-12-01 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_configuracioncodigootp_codigootp_conteo_intentos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigootp',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('VENCIDO', 'Inactivo'), ('EXITOSO', 'Validado'), ('INVALIDO', 'Invalido')], default='ACTIVO', max_length=10),
        ),
    ]
