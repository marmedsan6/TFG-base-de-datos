from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from plantasapi.serializers import ImageSerializer, PlantaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class InfoPlantasMocked(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Obtienes tus datos de plantas',
        request = ImageSerializer,
        responses={200: PlantaSerializer(many=True)}
    )
    def obtener_info_plantas(self, request, *args, **kwargs):
        return Response([
  {
    "id": 1,
    "common_name": "Olive",
    "scientific_name": "Olea europaea",
    "image_url": "https://bs.plantnet.org/image/o/de82f7f1a82590515b6c24c36fb52c0c745751d6",
    "ph_maximum": 7,
    "ph_minimum": 6.5,
    "light": 8
  },
  {
    "id": 2,
    "common_name": "Cork oak",
    "scientific_name": "Quercus suber",
    "image_url": "https://bs.plantnet.org/image/o/18d98dce42b463a97cca4e642ab61aecce8c74f6",
    "ph_maximum": 5.5,
    "ph_minimum": 5,
    "light": 8
  },
  {
    "id": 8,
    "common_name": "Hardee peppertree",
    "scientific_name": "Schinus polygama",
    "image_url": "https://bs.plantnet.org/image/o/3cd99f0c5725e24b529b97064e0cc44473a8d9da",
    "ph_maximum": None,
    "ph_minimum": None,
    "light": None
  }
], status=status.HTTP_200_OK)