"""
URL configuration for PPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    #  URLs de la aplicación myPPG 
    path('', include('myPPG.urls')),

    # Redirecciones
    path('index.html', RedirectView.as_view(url='/', permanent=True)),
    path('productos.html', RedirectView.as_view(url='/productos/', permanent=True)),
    path('perfil.html', RedirectView.as_view(url='/perfil/', permanent=True)),
    path('login.html', RedirectView.as_view(url='/login/', permanent=True)),
    path('registro.html', RedirectView.as_view(url='/registro/', permanent=True)),
    path('recuperar.html', RedirectView.as_view(url='/recuperar/', permanent=True)),
    path('carrito.html', RedirectView.as_view(url='/carrito/', permanent=True)),
    path('admin.html', RedirectView.as_view(url='/admin-panel/', permanent=True)),

    # redirecciones para categorías antiguas
    path('categoria-accion.html', RedirectView.as_view(url='/categoria/accion/', permanent=True)),
    path('categoria-aventura.html', RedirectView.as_view(url='/categoria/aventura/', permanent=True)),
    path('categoria-deportes.html', RedirectView.as_view(url='/categoria/deportes/', permanent=True)),
    path('categoria-carreras.html', RedirectView.as_view(url='/categoria/carreras/', permanent=True)),
    path('categoria-indie.html', RedirectView.as_view(url='/categoria/indie/', permanent=True)),
]