from rest_framework import serializers
from .models import Historial
from rest_framework import serializers

class HistorialSerializer(serializers.ModelSerializer):
    info_planta = serializers.SerializerMethodField() #Con esto no hace falta crear get_info_planta en otra clase
    class Meta:
        model = Historial
        fields = ['id', 'fecha', 'usuario', 'nombre_cientifico_planta', 'url_foto']

class PlantaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    common_name = serializers.CharField(max_length=100)
    scientific_name = serializers.SerializerMethodField()
    cycle = serializers.CharField(max_length=50)
    watering = serializers.CharField(max_length=50)
    watering_general_benchmark = serializers.SerializerMethodField()
    sunlight = serializers.SerializerMethodField()
    flowers = serializers.BooleanField()
    fruits = serializers.BooleanField()
    growth_rate = serializers.CharField(max_length=50)
    maintenance = serializers.CharField(max_length=50)
    medicinal = serializers.BooleanField()
    poisonous_to_humans = serializers.BooleanField()
    poisonous_to_pets = serializers.BooleanField()
    description = serializers.CharField(max_length=1000)
    original_url = serializers.SerializerMethodField()

    def get_scientific_name(self, obj):
        # Obtener el primer nombre científico de la lista
        return obj.get('scientific_name', [None])[0]

    def get_watering_general_benchmark(self, obj):
        # Extraer el valor y la unidad del benchmark general de riego
        benchmark = obj.get('watering_general_benchmark', {})
        return {
            "value": benchmark.get('value', None),
            "unit": benchmark.get('unit', None)
        }

    def get_sunlight(self, obj):
        # Obtener el primer tipo de luz solar de la lista
        return obj.get('sunlight', [None])[0]

    def get_original_url(self, obj):
        # Obtener la URL original de la imagen
        image_data = obj.get('default_image', {})
        return image_data.get('original_url', None)
