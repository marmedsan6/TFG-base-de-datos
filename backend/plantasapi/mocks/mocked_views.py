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
                        "common_name": "Shirley poppy",
                        "duration": None,
                        "edible": False,
                        "family": "Papaveraceae",
                        "flower": {
                            "color": None
                        },
                        "growth": {
                            "light": 8,
                            "ph_maximum": 7.5,
                            "ph_minimum": 7
                        },
                        "id": 127170,
                        "image_url": "https://bs.plantnet.org/image/o/401c147ff21437f2cc7a1629ca7afafdd07e1eeb",
                        "scientific_name": "Papaver rhoeas",
                        "specifications": {
                            "growth_form": None,
                            "growth_habit": "Forb/herb",
                            "growth_rate": None
                        }
                    },
                    {
                        "common_name": "Long-head poppy",
                        "duration": None,
                        "edible": False,
                        "family": "Papaveraceae",
                        "flower": {
                            "color": None
                        },
                        "growth": {
                            "light": 8,
                            "ph_maximum": 5.5,
                            "ph_minimum": 5
                        },
                        "id": 127060,
                        "image_url": "https://bs.plantnet.org/image/o/bbe185dbe68d149fc35ea0775628e688553ca104",
                        "scientific_name": "Papaver dubium",
                        "specifications": {
                            "growth_form": None,
                            "growth_habit": "Forb/herb",
                            "growth_rate": None
                        }
                    }
                ], status=status.HTTP_200_OK)