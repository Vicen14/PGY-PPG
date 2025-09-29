from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField() 
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True) # relación con categoria
    imagen = models.CharField(max_length=200, blank=True, null=True) # URL de la imagen

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f'Pedido #{self.id} de {self.usuario.username}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}'