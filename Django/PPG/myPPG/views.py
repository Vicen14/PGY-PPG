from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Categoria, Pedido
from .forms import RegistroPersonalizadoForm, EditarPerfilForm, ProductoForm, CategoriaForm

# vistas principales y de productos

def index(request):
    """ Muestra la página de inicio. """
    return render(request, 'funcionalidades/index.html')

def lista_productos(request):
    """ Muestra todos los productos obtenidos de la base de datos. """
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'funcionalidades/productos.html', context)

# vistas de Autenticación

def registro(request):
    """ Lógica para registrar nuevos usuarios. """
    if request.method == 'POST':
        form = RegistroPersonalizadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
            messages.success(request, "Registro completado. Bienvenido.")
            return redirect('perfil')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroPersonalizadoForm()
    return render(request, 'funcionalidades/registro.html', {'form': form})

def login_view(request):
    """ Lógica para iniciar sesión. """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Has iniciado sesión correctamente.")
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'funcionalidades/login.html', {'form': form})

def logout_view(request):
    """ Cierra la sesión del usuario. """
    logout(request)
    return redirect('index')

def recuperar(request):
    """ Muestra la página para recuperar contraseña. """
    return render(request, 'funcionalidades/recuperar.html')


# vistas de Perfil de Usuario

@login_required
def perfil(request):
    """ Muestra el perfil del usuario que ha iniciado sesión. """
    return render(request, 'funcionalidades/perfil.html')

@login_required
def editar_perfil(request):
    """ Lógica para que el usuario edite su información. """
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'funcionalidades/editar_perfil.html', {'form': form})


# vistas del Carrito de Compras

@login_required
def ver_carrito(request):
    """ Muestra el contenido del carrito guardado en la sesión. """
    carrito = request.session.get('carrito', {})
    context = {'carrito': carrito}
    return render(request, 'funcionalidades/carrito.html', context)

@login_required
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

@login_required
def eliminar_del_carrito(request, producto_id):
    """ Elimina un producto del carrito en la sesión. """
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def limpiar_carrito(request):
    """ Elimina todos los productos del carrito. """
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('carrito')

@login_required
def checkout(request):
    """ Lógica para procesar la compra. """
    return render(request, 'funcionalidades/checkout.html')

# vistas de Categorías

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

# función para verificar si es admin
def es_admin(user):
    return user.is_staff

# vistas de administración
@login_required
@user_passes_test(es_admin)
def admin_crear_producto(request):
    """ Vista para crear productos (solo admin) """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('admin_panel')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ProductoForm()
    return render(request, 'admin/crear_producto.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def admin_crear_categoria(request):
    """ Vista para crear categorías (solo admin) """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('admin_panel')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = CategoriaForm()
    return render(request, 'admin/crear_categoria.html', {'form': form})

# vista para el Panel de Admin Personalizado
@login_required
def admin_panel(request):
    """ Muestra el panel de administración personalizado. """
    return render(request, 'funcionalidades/admin.html')