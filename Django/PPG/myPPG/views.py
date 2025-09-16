from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Product, Category, Profile, Order, OrderItem, InventoryMovement
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


# ---------- HOME ----------
def index(request):
    return render(request, "funcionalidades/index.html")

# ---------- AUTH ----------
def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            messages.success(request, "Has iniciado sesión.")
            return redirect("index")
        messages.error(request, "Credenciales incorrectas.")
    return render(request, "funcionalidades/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("index")

def registro_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email',''),
                password=form.cleaned_data['password']
            )
            Profile.objects.create(user=user, role='cliente')
            messages.success(request, 'Usuario registrado con éxito.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'funcionalidades/registro.html', {'form': form})

def recuperar_view(request):
    return render(request, "funcionalidades/recuperar.html")  # placeholder

# ---------- PRODUCTOS ----------
def product_list(request):
    categoria = request.GET.get('cat')
    qs = Product.objects.filter(active=True)
    if categoria:
        qs = qs.filter(category__slug=categoria)
    return render(request, "funcionalidades/productos.html", {"productos": qs})

def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk, active=True)
    return render(request, "funcionalidades/producto_detalle.html", {"p": p})

# ---------- CARRITO ----------
def _get_cart(session):
    cart = session.get('cart', {})
    session['cart'] = cart
    return cart

def _cart_totals(cart):
    items, total = [], Decimal('0')
    for pid, qty in cart.items():
        prod = Product.objects.filter(id=int(pid), active=True).first()
        if not prod: continue
        line_total = Decimal(qty) * prod.price
        items.append({"product": prod, "qty": qty, "unit_price": prod.price, "line_total": line_total})
        total += line_total
    return items, total

def cart_view(request):
    items, total = _cart_totals(_get_cart(request.session))
    return render(request, "funcionalidades/carrito.html", {"items": items, "total": total})

@login_required
def cart_add(request, pk):
    prod = get_object_or_404(Product, pk=pk, active=True)
    qty = int(request.POST.get('qty', 1))
    cart = _get_cart(request.session)
    cart[str(prod.id)] = cart.get(str(prod.id), 0) + qty
    request.session.modified = True
    messages.success(request, f"{prod.title} añadido al carrito.")
    return redirect('carrito')

@login_required
def cart_remove(request, pk):
    cart = _get_cart(request.session)
    cart.pop(str(pk), None)
    request.session.modified = True
    return redirect('carrito')

@login_required
def cart_update(request, pk):
    qty = max(0, int(request.POST.get('qty', 1)))
    cart = _get_cart(request.session)
    if qty == 0: cart.pop(str(pk), None)
    else: cart[str(pk)] = qty
    request.session.modified = True
    return redirect('carrito')

@login_required
def order_create(request):
    cart = _get_cart(request.session)
    items, total = _cart_totals(cart)
    if not items:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')

    order = Order.objects.create(user=request.user, total=total, status='pendiente')
    for it in items:
        OrderItem.objects.create(order=order, product=it['product'], quantity=it['qty'], unit_price=it['unit_price'])
        it['product'].stock = max(0, it['product'].stock - it['qty'])
        it['product'].save(update_fields=['stock'])
        InventoryMovement.objects.create(product=it['product'], quantity_change=-int(it['qty']), reason='venta')

    request.session['cart'] = {}
    messages.success(request, f"Orden #{order.id} creada. Total: ${total}")
    return redirect('index')
