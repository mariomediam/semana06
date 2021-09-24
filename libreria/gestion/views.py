from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ProductoModel
from .serializers import ProductoSerializer
from rest_framework import status

class PruebaController(APIView):
    def get(self, request, format=None):
        return Response(data={'mensaje':'exito'}, status=200)

    def post(self, request:Request, format=None):
        print(request.data)
        return Response(data={'mensaje':'Hiciste post'})

#class ProductosController(ListAPIView):
#    queryset = ProductoModel.objects.all()
#    serializer_class = ProductoSerializer


#class ProductosController(CreateAPIView):
#    queryset = ProductoModel.objects.all()
#    serializer_class = ProductoSerializer

class ProductosController(ListCreateAPIView):
    queryset = ProductoModel.objects.all()
    serializer_class = ProductoSerializer

    def get(self, request):
        respuesta = self.get_queryset()
        print(respuesta)
        #instance cuando ya tenemos informacion en BD y lka queremos serializar para moratrasela al cliente
        #data para si la informacion que me envia el cliente esta buena
        #many indica que estamos pasando una lista de instancias
        
        respuesta_serializada = self.serializer_class(instance=respuesta, many=True)
        
        print(respuesta_serializada)
        
        return Response(data={"message":None, "content":respuesta_serializada.data})

    def post(self, request:Request):
        print(request.data)
        data = self.serializer_class(data=request.data)
        #data.is_valid(raise_exception=True)
        if data.is_valid():
            data.save()
            return Response(data={"message":None, "content":data.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"Error al guardar el producto",
                    "content":data.errors}, status=status.HTTP_400_BAD_REQUEST
            )

class ProductoController(APIView):
    def get(self, request, id):
        #print(id)
        producto_encontrado = ProductoModel.objects.filter(produtoId=id).first()
        print("xxxxx")
        if producto_encontrado:
            serializador = ProductoSerializer(instance=producto_encontrado)
            return Response(data={"message":None, "content": serializador.data})
        else:
            return Response(data={"message":"Producto no existe"}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, id):
        producto_encontrado = ProductoModel.objects.filter(produtoId=id).first()
        if producto_encontrado:            
            serializador = ProductoSerializer(data=request.data)
            if serializador.is_valid():                    
                serializador.update(instance=producto_encontrado, validated_data=serializador.validated_data)
                return Response(data={"message":"Producto actualizado exitosamente", "content": serializador.data})
            else:
                return Response(data={"message":"Error al actualizar el producto", "content":serializador.errors}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response(data={"message":"Producto no existe"}, status=status.HTTP_404_NOT_FOUND)

        

    def delete(self, request):
        pass