import time
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from plantasapi.serializers import ImageSerializer, LoginSerializer, PlantaSerializer, TokenSerializer, RegisterSerializer
from .plant_id import PlantID
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class InfoPlantas(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Obtienes tus datos de plantas',
        request = ImageSerializer,
        responses={200: PlantaSerializer(many=True)}
    )
    def obtener_info_plantas(self, request, *args, **kwargs):
        #image = request.data['base64Img']
        #print(image)
        serializer_img = ImageSerializer(data=request.data)
        if serializer_img.is_valid():
            image = serializer_img.validated_data['base64Img']

        nombre_plantas = self.identificar_planta(image)
        api_key = '3-kiaGeQ4pf2MNHc5kS44oKjw2HFW-Ys5_O8GlC-Jt8'
        plantas_datos = []

        for nombre in nombre_plantas:
            try:
                q = "Abies alba"
                
                species_list_url = f'https://trefle.io/api/v1/plants/search?token={api_key}&q={nombre}' 
                species_endpoint = requests.get(species_list_url).json()

                plant_id = species_endpoint['data'][0]['links']['self'] 
                plant_details_url = f'https://trefle.io/{plant_id}?token={api_key}'

                response = requests.get(plant_details_url)

                response.raise_for_status()
                plant_data = response.json()
                print(plant_data)

                plantas_datos.append(plant_data['data'])
                
                
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e), 'content': str(e.response.content)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        serializer = PlantaSerializer(plantas_datos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def identificar_planta(self, base64Img):
        api_key = 'uT96MaWiW3soVsf2AONBpZoK07pgL6MdfkSriyhAZSKgSLEfMk'  

        client = PlantID(api_key=api_key)
        
        plant_data = client.identify_plant(image_base64=base64Img)
            
        if plant_data and 'result' in plant_data.keys() and 'classification' in plant_data['result'].keys() and 'suggestions' in plant_data['result']['classification'].keys():
            
            suggestions = plant_data['result']['classification']['suggestions'][0:3]
            scientific_names = map(lambda suggestion: suggestion['name'] , suggestions)
            
            return scientific_names
        else:
            raise requests.exceptions.RequestException("No se ha encontrado la planta")

class IniciarSesion(viewsets.ViewSet):        
# login
    @extend_schema(
        description='Login',
        request=LoginSerializer,
        responses={200: TokenSerializer},
        methods=['POST']
    )
    def login(self, request):
        print(make_password('test'))
        cuenta_data = request.data
        try:
            user = authenticate(username=cuenta_data["username"], password=cuenta_data["password"])
            if user is not None:
                return Response({"token":  'Token ' + AuthToken.objects.create(user=user)[1]}, content_type='application/json', status=200)
            else:
                raise requests.exceptions.RequestException("No se ha encontrado el usuario")
        except User.DoesNotExist:
            raise requests.exceptions.RequestException("No se ha encontrado el usuario")

    @extend_schema(
        description='Crea una cuenta',
        request=RegisterSerializer,
        responses={201: TokenSerializer},
        methods=['POST']
    )    

    def register(self, request):
        cuenta_data = request.data
    
        cuenta_data["is_staff"] = False
        cuenta_data["is_superuser"] = False
        cuenta_data["is_active"] = True
        cuenta_data["password"] = make_password(cuenta_data["password"])

        cuenta: User = User(**cuenta_data)
        cuenta.full_clean()
        cuenta.save()
        return JsonResponse({"message": "Usuario registrado exitosamente"}, content_type='application/json', status=201)