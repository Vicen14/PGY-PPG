"""
URL configuration for PPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from myPPG import views
from django.contrib.auth import views as auth_views # importamos las vistas de autenticación de Django
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

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

    # Rutas directas a las plantillas HTML (sirven las plantillas sin pasar por la vista)
    path('funcionalidades/index.html', TemplateView.as_view(template_name='funcionalidades/index.html'), name='index_html_direct'),
    path('funcionalidades/registro.html', TemplateView.as_view(template_name='funcionalidades/registro.html'), name='registro_html_direct'),
    path('funcionalidades/login.html', TemplateView.as_view(template_name='funcionalidades/login.html'), name='login_html_direct'),
    path('funcionalidades/recuperar.html', TemplateView.as_view(template_name='funcionalidades/recuperar.html'), name='recuperar_html_direct'),
    path('funcionalidades/perfil.html', TemplateView.as_view(template_name='funcionalidades/perfil.html'), name='perfil_html_direct'),
    path('funcionalidades/editar_perfil.html', TemplateView.as_view(template_name='funcionalidades/editar_perfil.html'), name='editar_perfil_html_direct'),
    path('funcionalidades/carrito.html', TemplateView.as_view(template_name='funcionalidades/carrito.html'), name='carrito_html_direct'),
    path('funcionalidades/checkout.html', TemplateView.as_view(template_name='funcionalidades/checkout.html'), name='checkout_html_direct'),
    path('funcionalidades/admin.html', TemplateView.as_view(template_name='funcionalidades/admin.html'), name='admin_panel_html_direct'),


    path('categorias/categoria-accion.html', TemplateView.as_view(template_name='categorias/categoria-accion.html'), name='categoria_accion_html_direct'),
    path('categorias/categoria-aventura.html', TemplateView.as_view(template_name='categorias/categoria-aventura.html'), name='categoria_aventura_html_direct'),
    path('categorias/categoria-deportes.html', TemplateView.as_view(template_name='categorias/categoria-deportes.html'), name='categoria_deportes_html_direct'),
    path('categorias/categoria-carreras.html', TemplateView.as_view(template_name='categorias/categoria-carreras.html'), name='categoria_carreras_html_direct'),
    path('categorias/categoria-indie.html', TemplateView.as_view(template_name='categorias/categoria-indie.html'), name='categoria_indie_html_direct'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    # Si usas MEDIA, añade también:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_DIR / 'media')