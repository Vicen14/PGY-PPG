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
from django.urls import path
from myPPG import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend pages (serve the templates directly)
    path('', views.index, name='index'),
    path('index.html', views.index, name='index_html'),
    path('productos.html', views.productos, name='productos'),
    path('perfil.html', views.perfil, name='perfil'),
    path('login.html', views.login_view, name='login'),
    path('registro.html', views.registro, name='registro'),
    path('recuperar.html', views.recuperar, name='recuperar'),
    path('carrito.html', views.carrito, name='carrito'),
    path('admin.html', views.admin_panel, name='admin_panel'),

    # Category pages
    path('categoria-accion.html', views.categoria_accion, name='categoria_accion'),
    path('categoria-aventura.html', views.categoria_aventura, name='categoria_aventura'),
    path('categoria-deportes.html', views.categoria_deportes, name='categoria_deportes'),
    path('categoria-carreras.html', views.categoria_carreras, name='categoria_carreras'),
    path('categoria-indie.html', views.categoria_indie, name='categoria_indie'),
]
