from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Producto, Categoria # Asegúrate de importar tus modelos

# --------------------------------------------------------------------------
#  Vistas Principales y de Productos
# --------------------------------------------------------------------------

def index(request):
    """ Muestra la página de inicio. """
    return render(request, 'funcionalidades/index.html')

def lista_productos(request):
    """ Muestra todos los productos obtenidos de la base de datos. """
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'funcionalidades/productos.html', context)

# --------------------------------------------------------------------------
#  Vistas de Autenticación
# --------------------------------------------------------------------------

def registro(request):
    """ Lógica para registrar nuevos usuarios. """
    if request.method == 'POST':
        # Aquí va la lógica para crear un nuevo usuario
        pass
    return render(request, 'funcionalidades/registro.html')

def login_view(request):
    """ Lógica para iniciar sesión. """
    if request.method == 'POST':
        # Aquí va la lógica para autenticar al usuario
        pass
    return render(request, 'funcionalidades/login.html')

def logout_view(request):
    """ Cierra la sesión del usuario. """
    logout(request)
    return redirect('index')

def recuperar(request):
    """ Muestra la página para recuperar contraseña. """
    return render(request, 'funcionalidades/recuperar.html')

# --------------------------------------------------------------------------
#  Vistas de Perfil de Usuario
# --------------------------------------------------------------------------

def perfil(request):
    """ Muestra el perfil del usuario que ha iniciado sesión. """
    # Aquí va la lógica para obtener los datos del usuario
    return render(request, 'funcionalidades/perfil.html')

def editar_perfil(request):
    """ Lógica para que el usuario edite su información. """
    if request.method == 'POST':
        # Aquí va la lógica para actualizar los datos del usuario
        pass
    # Debes crear una plantilla para editar el perfil o usar la misma.
    return render(request, 'funcionalidades/perfil.html')

# --------------------------------------------------------------------------
#  Vistas del Carrito de Compras
# --------------------------------------------------------------------------

def ver_carrito(request):
    """ Muestra el contenido del carrito guardado en la sesión. """
    carrito = request.session.get('carrito', {})
    context = {'carrito': carrito}
    return render(request, 'funcionalidades/carrito.html', context)

def agregar_al_carrito(request, producto_id):
    """ Agrega un producto al carrito en la sesión. """
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)

    if id_str in carrito:
        carrito[id_str]['cantidad'] += 1
    else:
        carrito[id_str] = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1,
            'imagen': producto.imagen if producto.imagen else ''
        }
    
    request.session['carrito'] = carrito
    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    """ Elimina un producto del carrito en la sesión. """
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
    return redirect('carrito')

def limpiar_carrito(request):
    """ Elimina todos los productos del carrito. """
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('carrito')

def checkout(request):
    """ Lógica para procesar la compra. """
    # Aquí iría la lógica para crear un objeto Pedido en la BD
    return render(request, 'ruta/a/checkout.html') # Necesitas crear esta plantilla

# --------------------------------------------------------------------------
#  Vistas de Categorías
# --------------------------------------------------------------------------

def categoria_accion(request):
    productos = Producto.objects.filter(categoria__nombre='Acción')
    context = {'productos': productos, 'categoria': 'Acción'}
    return render(request, 'categorias/categoria-accion.html', context)

def categoria_aventura(request):
    productos = Producto.objects.filter(categoria__nombre='Aventura')
    context = {'productos': productos, 'categoria': 'Aventura'}
    return render(request, 'categorias/categoria-aventura.html', context)

def categoria_deportes(request):
    productos = Producto.objects.filter(categoria__nombre='Deportes')
    context = {'productos': productos, 'categoria': 'Deportes'}
    return render(request, 'categorias/categoria-deportes.html', context)

def categoria_carreras(request):
    productos = Producto.objects.filter(categoria__nombre='Carreras')
    context = {'productos': productos, 'categoria': 'Carreras'}
    return render(request, 'categorias/categoria-carreras.html', context)

def categoria_indie(request):
    productos = Producto.objects.filter(categoria__nombre='Indie')
    context = {'productos': productos, 'categoria': 'Indie'}
    return render(request, 'categorias/categoria-indie.html', context)

# --------------------------------------------------------------------------
#  Vista para el Panel de Admin Personalizado
# --------------------------------------------------------------------------

def admin_panel(request):
    """ Muestra el panel de administración personalizado. """
    return render(request, 'funcionalidades/admin.html')