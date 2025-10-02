from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Categoria, Pedido
from .forms import RegistroPersonalizadoForm, EditarPerfilForm, ProductoForm, CategoriaForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .services.rawg_service import RAWGService
from .models import Juego, Genero
import json

def registrar_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    campos_obligatorios = ['nombre', 'apellidos', 'correo', 'rol']
    for campo in campos_obligatorios:
        if campo not in data or not str(data.get(campo, '')).strip():
            return JsonResponse({'success': False, 'error': f'Campo {campo} es obligatorio.'}, status=400)

    password = (
        data.get('clave')
        or data.get('contraseña')
        or data.get('contraeña')
        or data.get('password')
    )
    if not password:
        return JsonResponse({'success': False, 'error': 'Campo contraseña es obligatorio.'}, status=400)

    if User.objects.filter(email=data['correo']).exists():
        return JsonResponse({'success': False, 'error': 'Correo ya registrado.'}, status=409)

    try:
        username = data['correo']
        if User.objects.filter(username=username).exists():
            base = username
            i = 1
            while User.objects.filter(username=f"{base}-{i}").exists():
                i += 1
            username = f"{base}-{i}"

        user = User.objects.create_user(
            username=username,
            first_name=str(data.get('nombre', '')).strip(),
            last_name=str(data.get('apellidos', '')).strip(),
            email=data['correo'],
            password=password,
        )

        rol = str(data.get('rol', '')).strip().lower()
        if rol in ('admin', 'staff'):
            user.is_staff = True
            user.save(update_fields=['is_staff'])

        return JsonResponse({'success': True, 'message': 'Usuario registrado correctamente en Oracle.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# vistas principales
def index(request):
    """Página de inicio con juegos de RAWG API"""
    try:
        juegos_populares = RAWGService.get_popular_games()
        featured_games = juegos_populares.get('results', [])[:8] if juegos_populares else []
    except Exception as e:
        print(f"Error al cargar juegos populares: {e}")
        featured_games = []
    
    context = {
        'featured_games': featured_games,
        'title': 'PixelPlay Games - Inicio'
    }
    return render(request, 'funcionalidades/index.html', context)

def lista_productos(request):
    """Muestra todos los productos de la base de datos Oracle"""
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'funcionalidades/productos.html', context)

# vistas de autenticación
def registro(request):
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
    logout(request)
    return redirect('index')

def recuperar(request):
    return render(request, 'funcionalidades/recuperar.html')

# perfil de usuario
@login_required
def perfil(request):
    return render(request, 'funcionalidades/perfil.html')

@login_required
def editar_perfil(request):
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

# carrito de compras
@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    context = {'carrito': carrito}
    return render(request, 'funcionalidades/carrito.html', context)

@login_required
def agregar_al_carrito(request, producto_id):
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
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def limpiar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('carrito')

@login_required
def checkout(request):
    return render(request, 'funcionalidades/checkout.html')

# categorias bd
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

# para ver si es admin
def es_admin(user):
    return user.is_staff

# admin panel y creación de productos y categorías
@login_required
@user_passes_test(es_admin)
def admin_crear_producto(request):
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

@login_required
def admin_panel(request):
    return render(request, 'funcionalidades/admin.html')

# VISTAS DE JUEGOS RAWG API 
def buscar_juegos(request):
    """Buscar juegos en RAWG API"""
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    
    games = []
    total_results = 0
    
    try:
        if query:
            results = RAWGService.search_games(query, page=page)
            if results:
                games = results.get('results', [])
                total_results = results.get('count', 0)
    except Exception as e:
        print(f"Error en búsqueda de juegos: {e}")
        messages.error(request, "Error al buscar juegos. Intenta nuevamente.")
    
    # paginación
    paginator = Paginator(range(total_results), 20)
    page_obj = paginator.get_page(page)
    
    context = {
        'games': games,
        'query': query,
        'page_obj': page_obj,
        'total_results': total_results,
        'title': f'Búsqueda: {query}' if query else 'Buscar Juegos'
    }
    
    return render(request, 'funcionalidades/buscar-juegos.html', context)

def detalle_juego(request, game_id):
    """Detalle de un juego específico de RAWG"""
    try:
        game_data = RAWGService.get_game_details(game_id)
        
        if not game_data:
            return render(request, 'funcionalidades/404.html', status=404)
        
        context = {
            'game': game_data,
            'title': game_data.get('name', 'Detalle del Juego')
        }
        
        return render(request, 'funcionalidades/detalle-juego.html', context)
    except Exception as e:
        print(f"Error al cargar detalle del juego: {e}")
        messages.error(request, "Error al cargar los detalles del juego.")
        return redirect('buscar_juegos')