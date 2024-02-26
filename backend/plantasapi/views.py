from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from plantasapi.serializers import PlantaSerializer

class InfoPlantas(viewsets.ViewSet):

    @extend_schema(
        description='Obtienes tus datos de plantas',
        responses={200: PlantaSerializer}
    )
    def obtener_info_plantas(self, request, *args, **kwargs):
        try:
            q = "Abies alba"
            api_key = 'CLAVE'
            species_list_url = f'https://perenual.com/api/species-list?key={api_key}&q={q}'
            species_list = requests.get(species_list_url).json()

            plant_id = species_list.data[0].id #Lo unico que puede fallar por sintaxis
            plant_details_url = f'https://perenual.com/api/species/details/{plant_id}?key={api_key}'
        
            response = requests.get(plant_details_url)
            response.raise_for_status()
            plant_data = response.json()
            serializer = PlantaSerializer(data=plant_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)