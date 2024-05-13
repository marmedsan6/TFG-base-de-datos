from datetime import timedelta
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from plantasapi.models import Historial, PlantInfo, ConfigurarPlantaUsuario
from plantasapi.serializers import BuscarPorNombreCientifico, ConfigPlantaUsuario, HistorialSerializer, IdConfig, IdSerializer, ImageSerializer, LoginSerializer, ModificarFrecuenciaSerializer, PlantaSerializer, TokenSerializer, RegisterSerializer, BuscarNombreCientifico
from .plant_id import PlantID
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone

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

        for planta in nombre_plantas:
            try:
                plant_info = PlantInfo.objects.filter(scientific_name=planta).first()
                if plant_info:
                    plantas_datos.append(plant_info)
                else:
                    species_list_url = f'https://trefle.io/api/v1/plants/search?token={api_key}&q={planta}' 
                    species_endpoint = requests.get(species_list_url).json()

                    plant_id = species_endpoint['data'][0]['id']
                    plant_details_url = f'https://trefle.io/api/v1/plants/{plant_id}?token={api_key}'

                    response = requests.get(plant_details_url)
                    response.raise_for_status()
                    plant_data = response.json()['data']

                    plant_info = PlantInfo(
                        scientific_name=plant_data['scientific_name'],
                        common_name=plant_data['common_name'],
                        light=plant_data['main_species']['growth']['light'],
                        ph_minimum=plant_data['main_species']['growth']['ph_minimum'],
                        ph_maximum=plant_data['main_species']['growth']['ph_maximum'],
                        image_url=plant_data['image_url']
                    )
                    plant_info.save()
                    plantas_datos.append(plant_info)
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e), 'content': str(e.response.content)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        serializer = PlantaSerializer(plantas_datos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def identificar_planta(self, base64Img):
        api_key = 'WfXhxzf2wYI5CIalVI2Are6R8HvfewXB4rZ8kGliSUwJfNhJiK'  

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
                return Response({"Error": "No se ha encontrado el usuario"}, content_type='application/json', status=404)
        except User.DoesNotExist:
            return Response({"Error": "No se ha encontrado el usuario"}, content_type='application/json', status=404)

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
    

class HistorialPlantas(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Añadir planta a historial',
        request= BuscarPorNombreCientifico,
        responses={200: IdConfig},
        methods=['POST']
    )

    def agregarPlanta(self, request):
        usuario = request.user
        scientific_name = request.data.get('scientific_name')
        
        planta = PlantInfo.objects.filter(scientific_name=scientific_name).first()

        configuracion_planta_usuario = ConfigurarPlantaUsuario(planta=planta)

        configuracion_planta_usuario.save()

        id_config = configuracion_planta_usuario.id

        historial = Historial(usuario=usuario, planta_usuario=configuracion_planta_usuario)

        historial.save()

        return JsonResponse({"message": "Planta registrada", "id_planta_usuario": id_config}, status=201)
        #registro_historial = Historial(**datos_historial)

        #registro_historial.full_clean()
        #registro_historial.save()
        #return JsonResponse({"message": "Planta registrada"}, status=201)

    @extend_schema(
        description='Obtener la configuracion de la planta del usuario',
        responses={200: ConfigPlantaUsuario},
        methods=['GET']
    )

    def obtenerConfigUsuario(self, request, id_planta_usuario):
        #id_config = request.data.get('id_planta_usuario')

        configuracion_planta_usuario = ConfigurarPlantaUsuario.objects.get(id=id_planta_usuario)

        serializer = ConfigPlantaUsuario(configuracion_planta_usuario)
        
        return Response(serializer.data)

    @extend_schema(
        description='Extraer los datos del historial',
        responses={200: HistorialSerializer(many=True)},
        methods=['GET']
    )

    def extraerHistorial(self, request):
        user=request.user
        plantas = list(Historial.objects.filter(usuario_id=user))
        return JsonResponse(HistorialSerializer(plantas, many=True).data, content_type='application/json', safe=False)
        
    @extend_schema(
        description='Indicar que una planta ha sido regada y actualizar la próxima fecha de riego',
        responses={200: ConfigPlantaUsuario},
        methods=['POST']
    )

    def plantaRegada(self, request, id_planta_usuario): 
        planta = ConfigurarPlantaUsuario.objects.get(id=id_planta_usuario)
        planta.fecha_riego = timezone.now() + timedelta(days=planta.frecuenciaRiego)
        planta.save()
        return Response(ConfigPlantaUsuario(planta).data, status=status.HTTP_200_OK)
        

    @extend_schema(
        description='Indicar que una planta ha sido pulverizada y actualizar la próxima fecha de pulverizacion',
        responses={200: HistorialSerializer},
        methods=['POST']
    )

    def plantaPulverizada(self, request, id_planta_usuario): 
        planta = ConfigurarPlantaUsuario.objects.get(id=id_planta_usuario)
        planta.fecha_pulverizacion = timezone.now() + timedelta(days=planta.frecuenciaPulverizacion)
        planta.save()
        return Response(ConfigPlantaUsuario(planta).data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Indicar que una planta ha sido fertilizada y actualizar la próxima fecha de fertilizacion',
        responses={200: HistorialSerializer},
        methods=['POST']
    )

    def plantaFertilizada(self, request, id_planta_usuario): 
        planta = ConfigurarPlantaUsuario.objects.get(id=id_planta_usuario)
        planta.fecha_fertilizacion = timezone.now() + timedelta(days=planta.frecuenciaFertilizacion)
        planta.save()
        return Response(ConfigPlantaUsuario(planta).data, status=status.HTTP_200_OK)
        
    @extend_schema(
        description='Modificar la frecuencia de riego, pulverización y fertilización de la planta del usuario',
        request=ModificarFrecuenciaSerializer,
        responses={200: ConfigPlantaUsuario},
        methods=['PUT']
    )
    def editarPlantaUsuario(self, request, id_planta_usuario):
        configuracion_planta_usuario = ConfigurarPlantaUsuario.objects.get(id=id_planta_usuario)

        if 'frecuenciaRiego' in request.data:
                configuracion_planta_usuario.frecuenciaRiego = request.data['frecuenciaRiego']
        if 'frecuenciaPulverizacion' in request.data:
                configuracion_planta_usuario.frecuenciaPulverizacion = request.data['frecuenciaPulverizacion']
        if 'frecuenciaFertilizacion' in request.data:
                configuracion_planta_usuario.frecuenciaFertilizacion = request.data['frecuenciaFertilizacion']

        configuracion_planta_usuario.save()

        serializer = ConfigPlantaUsuario(configuracion_planta_usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
