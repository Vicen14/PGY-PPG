from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # ---------- AUTENTICACIÓN ----------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('recuperar/', views.recuperar_view, name='recuperar'),

    # ---------- PRODUCTOS ----------
    path('productos/', views.product_list, name='productos'),
    path('producto/<int:pk>/', views.product_detail, name='producto_detalle'),

    # ---------- CARRITO ----------
    path('carrito/', views.cart_view, name='carrito'),
    path('carrito/agregar/<int:pk>/', views.cart_add, name='carrito_agregar'),
    path('carrito/eliminar/<int:pk>/', views.cart_remove, name='carrito_eliminar'),

    # Opcional: actualizar cantidades y crear orden
    path('carrito/actualizar/<int:pk>/', views.cart_update, name='carrito_actualizar'),
    path('orden/crear/', views.order_create, name='orden_crear'),
]
