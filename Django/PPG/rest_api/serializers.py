from rest_framework import serializers
from myPPG.models import ItemPedido, Juego

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'producto', 'cantidad', 'precio_unitario']

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ['rawg_id', 'nombre', 'slug', 'descripcion', 'fecha_lanzamiento', 'rating', 'plataformas', 'generos', 'etiquetas', 'desarrolladores', 'creadores', 'metacritic', 'imagen']