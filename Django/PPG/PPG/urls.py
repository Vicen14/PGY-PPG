"""
URL configuration for PPG project.
"""

from django.contrib import admin
from django.urls import path, include
from myPPG import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # panel de Admin Django
    path('admin/', admin.site.urls),

    # páginas principales
    path('', views.index, name='index'),
    path('productos/', views.lista_productos, name='productos'),

    # autenticación de usuarios 
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar/', views.recuperar, name='recuperar'),

    # perfil de Usuario
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # carrito de compras
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('checkout/', views.checkout, name='checkout'),

    # categorías (oracle)
    path('categoria/accion/', views.categoria_accion, name='categoria_accion'),
    path('categoria/aventura/', views.categoria_aventura, name='categoria_aventura'),
    path('categoria/deportes/', views.categoria_deportes, name='categoria_deportes'),
    path('categoria/carreras/', views.categoria_carreras, name='categoria_carreras'),
    path('categoria/indie/', views.categoria_indie, name='categoria_indie'),

    # panel de administración
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin/crear_producto/', views.admin_crear_producto, name='admin_crear_producto'),
    path('admin/crear_categoria/', views.admin_crear_categoria, name='admin_crear_categoria'),

    # RAWG API 
    path('buscar/', views.buscar_juegos, name='buscar_juegos'),
    path('juego/<int:game_id>/', views.detalle_juego, name='detalle_juego'),


    # API REST
    path('api/', include('rest_api.urls')),
]

# servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)