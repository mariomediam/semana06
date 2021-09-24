from django.contrib import admin
from .models import ClienteModel, ProductoModel

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):    
    list_display = ["produtoId", "productoNombre", "productoPrecio"]
    search_fields= ["productoNombre", "productoUnidadMedida"]
    list_filter = ["productoUnidadMedida"]
    readonly_fields =["produtoId"]



admin.site.register(ClienteModel)
admin.site.register(ProductoModel, ProductoAdmin)
