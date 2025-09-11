from django.shortcuts import render

# Create simple views that render the static templates in the app.
def index(request):
    return render(request, 'funcionalidades/index.html')

def productos(request):
    return render(request, 'funcionalidades/productos.html')

def perfil(request):
    return render(request, 'funcionalidades/perfil.html')

def login_view(request):
    return render(request, 'funcionalidades/login.html')

def registro(request):
    return render(request, 'funcionalidades/registro.html')

def recuperar(request):
    return render(request, 'funcionalidades/recuperar.html')

def carrito(request):
    return render(request, 'funcionalidades/carrito.html')

def admin_panel(request):
    return render(request, 'funcionalidades/admin.html')

# Category pages
def categoria_accion(request):
    return render(request, 'categorias/categoria-accion.html')

def categoria_aventura(request):
    return render(request, 'categorias/categoria-aventura.html')

def categoria_deportes(request):
    return render(request, 'categorias/categoria-deportes.html')

def categoria_carreras(request):
    return render(request, 'categorias/categoria-carreras.html')

def categoria_indie(request):
    return render(request, 'categorias/categoria-indie.html')