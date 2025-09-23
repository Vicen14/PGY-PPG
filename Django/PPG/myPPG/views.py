from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import Product, Category, Profile, Order, OrderItem, InventoryMovement
from .forms import RegistrationForm


# ---------- HOME ----------
def index(request):
    return render(request, "funcionalidades/index.html")


# ---------- AUTH: LOGIN CON EMAIL ----------
def login_view(request):
    """
    Permite iniciar sesión usando el CORREO electrónico.
    Si el formulario trae 'email', lo usa.
    Si el formulario trae 'username' pero contiene un correo, también lo interpreta como correo.
    Como fallback, acepta username normal.
    """
    if request.method == "POST":
        # Los templates a veces envían 'email' y otros 'username'. Tomamos ambos.
        raw_user = (
            request.POST.get("email")
            or request.POST.get("username")
            or ""
        ).strip()
        password = (request.POST.get("password") or "").strip()

        if not raw_user or not password:
            messages.error(request, "Debes ingresar correo/usuario y contraseña.")
            return render(request, "funcionalidades/login.html")

        User = get_user_model()
        user = None

        try:
            # 1) Intentar tratar el valor como correo (case-insensitive)
            user_obj = User.objects.get(email__iexact=raw_user)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            # 2) Si no existe ese correo, probar como username normal
            user = authenticate(request, username=raw_user, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Tu cuenta está inactiva.")
                return render(request, "funcionalidades/login.html")
            login(request, user)
            messages.success(request, "Has iniciado sesión.")
            return redirect("index")
        else:
            messages.error(request, "Credenciales incorrectas. Por favor, intenta nuevamente.")

    return render(request, "funcionalidades/login.html")


# ---------- AUTH: LOGOUT ----------
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("index")


# ---------- AUTH: REGISTRO ----------
def registro_view(request):
    """
    Registro básico usando tu RegistrationForm existente.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada. Ya puedes iniciar sesión.")
            return redirect("login")
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = RegistrationForm()

    return render(request, "funcionalidades/registro.html", {"form": form})


# ----------------------------------------------------------------------
# A PARTIR DE AQUÍ, SI TENÍAS OTRAS VISTAS (productos, carrito, perfil, etc.)
# LAS DEJO COMO STUBS/PLACEHOLDERS PARA NO ROMPER IMPORTS NI RUTAS.
# Puedes completarlas con tu lógica actual si las usas.
# ----------------------------------------------------------------------

def productos_view(request):
    productos = Product.objects.all().select_related("category")
    return render(request, "funcionalidades/productos.html", {"productos": productos})


@login_required
def perfil_view(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "funcionalidades/perfil.html", {"perfil": perfil})


# ----- Carrito (placeholders: ajusta a tu implementación si ya la tienes) -----

def cart_view(request):
    """
    Muestra el carrito almacenado en la sesión.
    Estructura de ejemplo en sesión:
    request.session['cart'] = { product_id: {"name": str, "qty": int, "price": "9.99"} }
    """
    cart = request.session.get("cart", {})
    total = sum(Decimal(item["price"]) * item["qty"] for item in cart.values())
    return render(request, "funcionalidades/carrito.html", {"cart": cart, "total": total})


def cart_add(request, product_id):
    """
    Añade 1 unidad del producto al carrito de sesión.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})
    item = cart.get(str(product_id), {"name": product.name, "qty": 0, "price": str(product.price)})
    item["qty"] += 1
    cart[str(product_id)] = item
    request.session["cart"] = cart
    messages.success(request, f"Se añadió {product.name} al carrito.")
    return redirect("carrito")


def cart_remove(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    messages.info(request, "Producto eliminado del carrito.")
    return redirect("carrito")
