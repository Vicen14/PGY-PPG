from django.db import models
from django.contrib.auth.models import User


# ---------- CATEGORY ----------
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


# ---------- PRODUCT ----------
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


# ---------- PROFILE ----------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


# ---------- ORDER ----------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden {self.id} de {self.user.username}"


# ---------- ORDER ITEM ----------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# ---------- INVENTORY MOVEMENT ----------
class InventoryMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    change = models.IntegerField(help_text="Cantidad agregada (+) o retirada (-)")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change} de {self.product.name} en {self.timestamp}"
