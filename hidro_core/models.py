from django.db import models
from django.contrib.auth.models import User

class Equipo(models.Model):
    
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
    
    equipo = models.ForeignKey(Equipo)
    temperatura = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    humedad = models.DecimalField(max_digits = 11, decimal_places = 2,null=True)
    intensidad_luz = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    temperatura_agua = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    viento = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    compaz_mag = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    acelerometro_x = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    acelerometro_y = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    acelerometro_z = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add = True)

class UmbralMedidaFisica(models.Model):
    nom_variable_fisica = models.CharField(max_length = 100, null=True)
    variable_fisica = models.CharField(max_length = 100, null=True)
    umbral_base = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_verde = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_amarillo = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)
    umbral_naranja = models.DecimalField(max_digits = 11, decimal_places = 2, null=True)

class Notificacion(models.Model):
    
    LEIDA = 'L'
    NO_LEIDA = 'NL'

    descripcion = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=2, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
