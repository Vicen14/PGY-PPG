from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myPPG.models import ItemPedido, Juego
from .serializers import ItemPedidoSerializer, JuegoSerializer

@csrf_exempt
@api_view(['GET', 'POST'])
def lista_items_pedido(request):
    if request.method == 'GET':
        items = ItemPedido.objects.all()
        serializer = ItemPedidoSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItemPedidoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
@api_view(['GET', 'POST'])
def lista_juegos(request):
    if request.method == 'GET':
        juegos = Juego.objects.all()
        serializer = JuegoSerializer(juegos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JuegoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)