from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'myppg_categoria'  # tabla específica para categorías

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField() 
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'myppg_producto'  # tabla específica para productos

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

    class Meta:
        db_table = 'myppg_pedido'  # tabla específica para pedidos

    def __str__(self):
        return f'Pedido #{self.id} de {self.usuario.username}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()

    class Meta:
        db_table = 'myppg_itempedido'  # tabla específica para items de pedido

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}'

# modelos para RAWG API 
class Juego(models.Model):
    # para que no se repitan usamos el id de rawg
    rawg_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True) 
    descripcion = models.TextField(blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    rating_top = models.IntegerField(default=5)
    imagen_fondo = models.URLField(max_length=500, blank=True, null=True)
    web_juego = models.URLField(max_length=500, blank=True, null=True)

    # para saber cuando creamos el modelo
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'myppg_juego' 
        ordering = ['-rating', 'nombre']

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    rawg_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True) 

    class Meta:
        db_table = 'myppg_genero' 

    def __str__(self):
        return self.nombre

class GeneroJuego(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='generos_juego')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    class Meta:
        db_table = 'myppg_generojuego'  
        unique_together = ['juego', 'genero']

    def __str__(self):
        return f'{self.juego.nombre} - {self.genero.nombre}'