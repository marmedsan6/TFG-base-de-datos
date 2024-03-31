"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plantasapi.views import InfoPlantas, IniciarSesion
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import RedirectView
from backend.scheme import KnoxTokenScheme # NO BORRAR, AUNQUE NO SE USE SINO SE PONE NO APARECE LA AUTENTICACIÓN EN EL SWAGGER

urlpatterns = [
    path('', RedirectView.as_view(url='/schema/swagger-ui/', permanent=True)),
    path('admin/', admin.site.urls),
    path('plantas/', InfoPlantas.as_view({'post': 'obtener_info_plantas'}), name='plantas'),
    path('login/', IniciarSesion.as_view({'post': 'login'}), name = 'login'),
    path('register/', IniciarSesion.as_view({'post': 'register'}), name = 'register'),

    # Swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
