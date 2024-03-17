from rest_framework import serializers
from .models import Historial
from rest_framework import serializers
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class HistorialSerializer(serializers.ModelSerializer):
    info_planta = serializers.SerializerMethodField() #Con esto no hace falta crear get_info_planta en otra clase
    class Meta:
        model = Historial
        fields = ['id', 'fecha', 'usuario', 'nombre_cientifico_planta', 'url_foto']

#class WateringGeneralBenchmarkSerializer(serializers.Serializer):
#    value = serializers.CharField(max_length=100, allow_null=True)
#    unit = serializers.CharField(max_length=100, allow_null=True)

class PlantaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    common_name = serializers.CharField(max_length=100)
    scientific_name = serializers.SerializerMethodField()
    family = serializers.CharField(max_length=50)
    image_url = serializers.SerializerMethodField()
    duration = serializers.CharField(max_length=50) #Duracion de vida de la planta, puede ser:- Annual: plants that live, reproduce, and die in one growing season.- Biennial: plants that need two growing seasons to complete their life cycle, normally completing vegetative growth the first year and flowering the second year.- Perennial: plants that live for more than two years, with the shoot system dying back to soil level each year.
    edible = serializers.BooleanField()
    sunlight = serializers.SerializerMethodField()
    #common_names(object) es una objeto, no sabria como extraer el dato pero es interesante para poner el nombre de la planta en español 
    #Mas datos interesantes pero que no se meterlos: Del campo Flower: color, Del campo specifications: growth_form, growth_habit, growth_rate, average_height, Del campo growth: ph_maximum, ph_mimimun, light, este es el campo mas interesante para el tratamiento pero la mayoria de datos normalmente no aparecen.
    #Ver más en: https://docs.trefle.io/docs/advanced/plants-fields
    watering_general_benchmark = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_scientific_name(self, obj):
        return obj.get('scientific_name', [None])[0]

    @extend_schema_field(WateringGeneralBenchmarkSerializer(many=False))
    def get_watering_general_benchmark(self, obj):
        benchmark = obj.get('watering_general_benchmark', {})
        return {
            "value": benchmark.get('value', None),
            "unit": benchmark.get('unit', None)
        }

    @extend_schema_field(OpenApiTypes.STR)
    def get_sunlight(self, obj):
        return obj.get('sunlight', [None])[0]

    @extend_schema_field(OpenApiTypes.URI)
    def get_original_url(self, obj):
        image_data = obj.get('default_image', {})
        return image_data.get('original_url', None)
    
class ImageSerializer(serializers.Serializer):
    base64Img = serializers.CharField()