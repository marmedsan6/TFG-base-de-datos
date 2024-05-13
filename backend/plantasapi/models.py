from django.db import models
from django.contrib.auth.models import User

class PlantInfo(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    scientific_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    light = models.CharField(max_length=255, null=True, blank=True)
    ph_minimum = models.FloatField(null=True)
    ph_maximum = models.FloatField(null=True)
    image_url = models.CharField(max_length = 255)

class ConfigurarPlantaUsuario(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(PlantInfo, null=False, on_delete=models.PROTECT)
    frecuenciaRiego = models.PositiveIntegerField(default=1) #Frecuencia de riego en días
    fecha_riego = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    frecuenciaPulverizacion = models.PositiveIntegerField(default=1)
    fecha_pulverizacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    frecuenciaFertilizacion = models.PositiveIntegerField(default=1)
    fecha_fertilizacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Historial(models.Model):
    id_planta_usuario = models.BigAutoField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, null=False, on_delete=models.PROTECT)
    planta_usuario = models.ForeignKey(ConfigurarPlantaUsuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
