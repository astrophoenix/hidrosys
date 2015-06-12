from django.db import models
from django.contrib.auth.models import User

class Equipo(models.Model):
    """ Modelo que representa un equipo de medición de datos
    """
    ACTIVO = 'A'
    INACTIVO = 'I'
    ESTADO = (
                (ACTIVO, "ACTIVO"),
                (INACTIVO,"INACTIVO"),
            )
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length = 100)
    estado = models.CharField(max_length = 1, default = ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add = True)
    fecha_modificacion = models.DateTimeField(auto_now = True)

class EquipoMedicion(models.Model):
    """ Modelo que representa cada valor medido de los sensores """
    equipo = models.ForeignKey(Equipo)
    temperatura = models.DecimalField(max_digits = 11, decimal_places = 2)
    humedad = models.DecimalField(max_digits = 11, decimal_places = 2)
    intensidad_luz = models.DecimalField(max_digits = 11, decimal_places = 2)
    temperatura_agua = models.DecimalField(max_digits = 11, decimal_places = 2)
    viento = models.DecimalField(max_digits = 11, decimal_places = 2)
    compaz_mag = models.DecimalField(max_digits = 11, decimal_places = 2)
    acelerometro_x = models.DecimalField(max_digits = 11, decimal_places = 2)
    acelerometro_y = models.DecimalField(max_digits = 11, decimal_places = 2)
    acelerometro_z = models.DecimalField(max_digits = 11, decimal_places = 2)
    fecha_creacion = models.DateTimeField(auto_now_add = True)


class UmbralMedidaFisica(models.Model):
    """ Modelo que define los umbrales para cada variable física medida."""
    nom_variable_fisica = models.CharField(max_length = 100)
    variable_fisica = models.CharField(max_length = 100)
    umbral_base = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_verde = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_amarillo = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_naranja = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
