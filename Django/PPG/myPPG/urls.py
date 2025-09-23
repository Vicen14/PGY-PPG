from django.urls import path
from . import views

app_name = 'myPPG'

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('perfil/', views.perfil, name='perfil'),
    path('carrito/', views.carrito, name='carrito'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('recuperar/', views.recuperar, name='recuperar'),
    
    # Panel de administración
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # Categorías (URLs limpias y organizadas)
    path('categoria/accion/', views.categoria_accion, name='categoria_accion'),
    path('categoria/aventura/', views.categoria_aventura, name='categoria_aventura'),
    path('categoria/deportes/', views.categoria_deportes, name='categoria_deportes'),
    path('categoria/carreras/', views.categoria_carreras, name='categoria_carreras'),
    path('categoria/indie/', views.categoria_indie, name='categoria_indie'),
]