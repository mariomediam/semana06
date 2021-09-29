from django.shortcuts import render
from django.utils.regex_helper import contains
from requests.sessions import PreparedRequest
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .models import CabeceraModel, DetalleModel, ProductoModel
from .serializers import ClienteSerializer, ProductoSerializer, OperacionSerializer, OperacionModelSerializer
from rest_framework import status
from .utils import PaginacionPersonalizada
from .models import ClienteModel
from rest_framework.serializers import Serializer
from os import environ
import requests as solicitudes
from django.db import transaction, Error
from datetime import datetime
from django.shortcuts import get_object_or_404

class PruebaController(APIView):
    def get(self, request, format=None):
        return Response(data={'mensaje':'exito'}, status=200)

    def post(self, request:Request, format=None):
        #print(request.data)
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
    pagination_class = PaginacionPersonalizada

    # def get(self, request):
    #     #respuesta = self.get_queryset()
    #     respuesta = self.get_queryset().filter(productoEstado=True).all()

    #     print(respuesta)
    #     #instance cuando ya tenemos informacion en BD y lka queremos serializar para moratrasela al cliente
    #     #data para si la informacion que me envia el cliente esta buena
    #     #many indica que estamos pasando una lista de instancias
        
    #     respuesta_serializada = self.serializer_class(instance=respuesta, many=True)
        
    #     print(respuesta_serializada)
        
    #     return Response(data={"message":None, "content":respuesta_serializada.data})

    def post(self, request:Request):
        #print(request.data)
        data = self.serializer_class(data=request.data)
        #data.is_valid(raise_exception=True)
        if data.is_valid():
            data.save()
            return Response(data={"message":"Producto creado exitosamente", "content":data.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":"Error al guardar el producto",
                    "content":data.errors}, status=status.HTTP_400_BAD_REQUEST
            )

class ProductoController(APIView):
    def get(self, request, id):
        producto_encontrado = ProductoModel.objects.filter(produtoId=id).first()
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

        

    def delete(self, request, id):
        producto_encontrado: ProductoModel = ProductoModel.objects.filter(produtoId=id).first()
        if producto_encontrado:            
            producto_encontrado.productoEstado = False
            producto_encontrado.save()
            serializador = ProductoSerializer(instance=producto_encontrado)
            return Response(data={"message":"Producto eliminado exitosamente", "content": serializador.data})            
        else:
            return Response(data={"message":"Producto no existe"}, status=status.HTTP_404_NOT_FOUND)

class ClienteController(CreateAPIView):
    queryset = ClienteModel.objects.all()
    serializer_class = ClienteSerializer

    def post(self, request:Request):
        data:Serializer = self.get_serializer(data=request.data)
        if data.is_valid():
            #validated_data es la data ya validada y se crea despues del evento is_valid()
            #initial_data lo que envía el cliente en el json
            #data es la data que coicnide con mi modelo pero sin validar si integridad
            #print(data.validated_data)
            documento=data.validated_data.get("clienteDocumento")
            direccion=data.validated_data.get("clienteDireccion")
            url="https://apiperu.dev/api/"
            if len(documento)==8:
                if direccion is None:
                    return Response(data={
                        "message":"Los clientes con DNI deben proveer la direccion"
                    }, status=status.HTTP_400_BAD_REQUEST)
                url += "dni/"
            elif len(documento)==11:
                url += "ruc/"
            resultado = solicitudes.get(url+documento, headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer " +environ.get("APIPERU_TOKEN")
            })
            #print(resultado.json())
            if resultado.json().get("success"):
                #grabo en BD
                data = resultado.json().get("data")
                nombre = data.get("nombre_completo") if data.get("nombre_completo") else data.get("nombre_o_razon_social")
                direccion = direccion if direccion else data.get("direccion_completa")
                nuevoCliente = ClienteModel(clienteNombre=nombre, clienteDocumento=documento, clienteDireccion=direccion)
                nuevoCliente.save()
                nuevo_cliente_serializado:Serializer = self.serializer_class(instance=nuevoCliente)
                return Response(data={
                    "message":"Cliente agregado exitosamente",
                    "contente": nuevo_cliente_serializado.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(data={
                    "message":"Documento incorrecto"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "message":"Error al ingresar el cliente",
                "content":data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class BuscadorClienteController(RetrieveAPIView):
    serializer_class = ClienteSerializer

    def get(self, request: Request):
        #print(request.query_params)
        documento = request.query_params.get('documento')
        nombre = request.query_params.get('nombre')

        if nombre and documento:
            clienteEncontrado = ClienteModel.objects.filter(
                clienteNombre__icontains=nombre).filter(clienteDocumento=documento).all()
        elif nombre:
            clienteEncontrado = ClienteModel.objects.filter(
                clienteNombre__icontains=nombre).all()
        elif documento:
            clienteEncontrado = ClienteModel.objects.filter(
                clienteDocumento=documento).all()
        else:
             return Response(data={
                    "message":"Debe de ingresar nombre y/o documento del cliente a buscar"
                }, status=status.HTTP_404_NOT_FOUND)

        data = self.serializer_class(instance=clienteEncontrado, many=True)

        return Response({'content': data.data}, status=status.HTTP_200_OK)


class OperacionController(CreateAPIView):
    serializer_class = OperacionSerializer

    def post(self, request: Request):
        data = self.serializer_class(data = request.data)
        if data.is_valid():
            #documento = request.data.get("cliente")
            documento=data.validated_data.get("cliente")

            clienteEncontrado = ClienteModel.objects.filter(
                clienteDocumento=documento).first()
            print(clienteEncontrado)
            detalles = data.validated_data.get("detalle")
            tipo = data.validated_data.get("tipo")
            
            try:
                with transaction.atomic():
                    if clienteEncontrado is None:
                        raise Exception("Cliente no existe")
                    nuevaCabecera=CabeceraModel(cabeceraTipo=tipo, clientes=clienteEncontrado)
                    nuevaCabecera.save()
                    print(nuevaCabecera)
                    for detalle in detalles:
                        producto = ProductoModel.objects.get(produtoId = detalle.get("producto"))
                        DetalleModel(detalleCantidad=detalle.get("cantidad"),
                            detalleImporte=producto.productoPrecio * detalle.get("cantidad"),
                            productos=producto,
                            cabeceras=nuevaCabecera).save()

            except Exception as e:
                print(e)
                return Response(data={
                    "messahe":"Error al crear la operacion",
                    "content": e.args
                })


            return Response(data={
                "message":"operacion registrada exitosamente"
            })
        else:
            return Response(data={
                "message": "Error al crear la operacion",
                "content": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class OperacionesController(RetrieveAPIView):
    serializer_class = OperacionModelSerializer

    def get(self, request:Request, id):
        #cabecera = CabeceraModel.objects.get(cabeceraId = id)
        cabecera = get_object_or_404(CabeceraModel, pk=id)
        print(cabecera)
        cabecera_serializada = self.serializer_class(instance=cabecera)
        print(cabecera_serializada)
        return Response(data={
            "message":"La operacion es",
            "content":cabecera_serializada.data
        })
