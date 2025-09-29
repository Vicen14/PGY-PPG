"""
URL configuration for PPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from myPPG import views
from django.contrib.auth import views as auth_views # importamos las vistas de autenticación de Django

urlpatterns = [

    #  panel de Administración de Django

    path('admin/', admin.site.urls),

    #  páginas Principales y Estáticas
    path('', views.index, name='index'), # Página de inicio
    path('index.html', views.index, name='index_html'), # Redirección por si se usa la URL completa
    path('productos/', views.lista_productos, name='productos'),

    #  autenticación de Usuarios 

    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), # Vista para cerrar sesión
    path('recuperar/', views.recuperar, name='recuperar'),


    #  perfil de Usuario

    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),


    #  carrito de Compras (Gestionado desde el backend)

    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('checkout/', views.checkout, name='checkout'), # Para procesar el pago


    #  páginas de Categorías

    path('categoria/accion/', views.categoria_accion, name='categoria_accion'),
    path('categoria/aventura/', views.categoria_aventura, name='categoria_aventura'),
    path('categoria/deportes/', views.categoria_deportes, name='categoria_deportes'),
    path('categoria/carreras/', views.categoria_carreras, name='categoria_carreras'),
    path('categoria/indie/', views.categoria_indie, name='categoria_indie'),


    path('admin_panel/', views.admin_panel, name='admin_panel'),
]