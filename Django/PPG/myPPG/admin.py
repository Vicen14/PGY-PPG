from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido
# Register your models here.
# Permite ver los productos dentro de la página de un pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # cuantos campos vacios para añadir productos se muestran
    readonly_fields = ('precio_unitario',) # el precio se debe tomar del producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """ Personalización para el modelo Categoria """
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """ Personalización para el modelo Producto """
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock') 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """ Personalización para el modelo Pedido """
    list_display = ('id', 'usuario', 'fecha_creacion', 'total', 'estado')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('usuario__username', 'id')
    readonly_fields = ('fecha_creacion', 'total', 'usuario') # campos que no se editan manualmente
    inlines = [ItemPedidoInline] # muestra los items del pedido dentro


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')