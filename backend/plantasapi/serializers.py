from rest_framework import serializers
from .models import Historial, ConfigurarPlantaUsuario
from rest_framework import serializers
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.models import User



#class WateringGeneralBenchmarkSerializer(serializers.Serializer):
#    value = serializers.CharField(max_length=100, allow_null=True)
#    unit = serializers.CharField(max_length=100, allow_null=True)
        
class ImageSerializer(serializers.Serializer):
    base64Img = serializers.CharField() #image_url = serializers.URLField(allow_blank=True, required=False)


class PlantaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    common_name = serializers.CharField(max_length=100)
    scientific_name = serializers.CharField(max_length=50)
    image_url = serializers.URLField()
    ph_maximum = serializers.FloatField()
    ph_minimum = serializers.FloatField()
    light = serializers.IntegerField()
    #common_names(object) es una objeto, no sabria como extraer el dato pero es interesante para poner el nombre de la planta en español 
    #Mas datos interesantes pero que no se meterlos: Del campo Flower: color, Del campo specifications: growth_form, growth_habit, growth_rate, average_height, Del campo growth: ph_maximum, ph_mimimun, light, este es el campo mas interesante para el tratamiento pero la mayoria de datos normalmente no aparecen.
    #Ver más en: https://docs.trefle.io/docs/advanced/plants-fields

    #@extend_schema_field(OpenApiTypes.STR)
    #def get_scientific_name(self, obj):
    #    return obj.get('scientific_name', [None])[0] #Para obtener el elemento 0 de la lista scientific_name
    


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class BuscarNombreCientifico(serializers.Serializer):
    frecuenciaRiego = serializers.IntegerField()
    frecuenciaPulverizacion = serializers.IntegerField()
    frecuenciaFertilizacion = serializers.IntegerField()

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class BuscarPorNombreCientifico(serializers.Serializer):
    scientific_name = serializers.CharField()

class IdConfig(serializers.Serializer):
    id_planta_usuario = serializers.IntegerField()

class ConfigPlantaUsuario(serializers.ModelSerializer):
    planta = PlantaSerializer()

    class Meta:
        model = ConfigurarPlantaUsuario
        fields = '__all__'

class HistorialSerializer(serializers.ModelSerializer):
    planta_usuario = ConfigPlantaUsuario()

    class Meta:
        model = Historial
        fields = '__all__'

class ModificarFrecuenciaSerializer(serializers.Serializer):
    frecuenciaRiego = serializers.IntegerField(required=False)
    frecuenciaPulverizacion = serializers.IntegerField(required=False)
    frecuenciaFertilizacion = serializers.IntegerField(required=False)