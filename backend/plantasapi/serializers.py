from rest_framework import serializers
from .models import Historial
from rest_framework import serializers
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.models import User

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = ['fecha', 'nombre_cientifico_planta', 'url_foto']

#class WateringGeneralBenchmarkSerializer(serializers.Serializer):
#    value = serializers.CharField(max_length=100, allow_null=True)
#    unit = serializers.CharField(max_length=100, allow_null=True)
        
class ImageSerializer(serializers.Serializer):
    base64Img = serializers.CharField() #image_url = serializers.URLField(allow_blank=True, required=False)

class FlowerSerializer(serializers.Serializer):
    color = serializers.ListField(child=serializers.CharField(), allow_empty=True)

class SpecificationsSerializer(serializers.Serializer):
    growth_form = serializers.CharField(max_length=50)
    growth_habit = serializers.CharField(max_length=50)
    growth_rate = serializers.CharField(max_length=50)

class GrowthSerializer(serializers.Serializer):
    ph_maximum = serializers.FloatField()
    ph_minimum = serializers.FloatField()
    light = serializers.IntegerField()


class PlantaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    common_name = serializers.CharField(max_length=100)
    scientific_name = serializers.CharField(max_length=50)
    family = serializers.CharField(max_length=50)
    image_url = serializers.URLField()
    duration = serializers.CharField(max_length=50) #Duracion de vida de la planta, puede ser:- Annual: plants that live, reproduce, and die in one growing season.- Biennial: plants that need two growing seasons to complete their life cycle, normally completing vegetative growth the first year and flowering the second year.- Perennial: plants that live for more than two years, with the shoot system dying back to soil level each year.
    edible = serializers.BooleanField()
    flower = FlowerSerializer()
    specifications = SpecificationsSerializer()
    growth = GrowthSerializer()
    #common_names(object) es una objeto, no sabria como extraer el dato pero es interesante para poner el nombre de la planta en español 
    #Mas datos interesantes pero que no se meterlos: Del campo Flower: color, Del campo specifications: growth_form, growth_habit, growth_rate, average_height, Del campo growth: ph_maximum, ph_mimimun, light, este es el campo mas interesante para el tratamiento pero la mayoria de datos normalmente no aparecen.
    #Ver más en: https://docs.trefle.io/docs/advanced/plants-fields

    #@extend_schema_field(OpenApiTypes.STR)
    #def get_scientific_name(self, obj):
    #    return obj.get('scientific_name', [None])[0] #Para obtener el elemento 0 de la lista scientific_name


    @extend_schema_field(OpenApiTypes.URI)
    def get_original_url(self, obj):
        image_data = obj.get('default_image', {})
        return image_data.get('original_url', None)
    

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
    nombreCientifico = serializers.CharField()
    fotoURL = serializers.CharField()
