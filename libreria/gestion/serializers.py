from django.db.models import fields
from rest_framework import serializers
from .models import ProductoModel

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        #fields = "__all__" hará uso de todos los atributos del modelo
        #fields = ['productoNombre','productoPrecio']
        fields='__all__'
        #exclude excluirá de la peticion como del retorno los atributos indicados
        #exclude = ['productoId']