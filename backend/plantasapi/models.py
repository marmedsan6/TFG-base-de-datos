from django.db import models
from django.contrib.auth.models import User

class Historial(models.Model):
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(User, null=False, on_delete=models.PROTECT)
    nombre_cientifico_planta = models.CharField(max_length = 100)
    url_foto = models.CharField(max_length = 255)