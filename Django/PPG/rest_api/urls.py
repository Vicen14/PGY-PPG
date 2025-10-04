from django.urls import path
from . import views


# api
urlpatterns = [
    path('pedido/', views.lista_items_pedido, name='lista_items_pedido'),
    path('juego/', views.lista_juegos, name='lista_juegos'),
]