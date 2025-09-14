from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin','Administrador'),
        ('cliente','Cliente'),
        ('vendedor','Vendedor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover = models.CharField(max_length=512, blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

