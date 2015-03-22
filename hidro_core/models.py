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
    temperatura = models.DecimalField(max_digits = 11, decimal_places = 2)
    humedad = models.DecimalField(max_digits = 11, decimal_places = 2)
    intensidad_luz = models.DecimalField(max_digits = 11, decimal_places = 2)
    fecha_creacion = models.DateTimeField(auto_now_add = True)
    