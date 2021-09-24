from django.db import models

# Create your models here.
class ProductoModel(models.Model):

    class opcionesUM(models.TextChoices):
        UNIDAD = "UN","UNIDAD"
        DOCENA = "DOC", "DOCENA"
        CIENTO = "CI", "CIENTO"
        MILLAR = "MI", "MILLAR"

    produtoId = models.AutoField(primary_key=True, null=False, unique=True, db_column="id")

    productoNombre = models.CharField(max_length=45, db_column="nombre,", null=False)

    productoPrecio = models.DecimalField(max_digits=10, decimal_places=2, db_column="precio")

    productoUnidadMedida = models.TextField(choices=opcionesUM.choices, default=opcionesUM.UNIDAD, db_column="unidad_medida")

    def __str__(self):
        return self.productoNombre

    class Meta:
        db_table="productos"
        ordering=["-productoPrecio"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

class ClienteModel(models.Model):
    clienteId = models.AutoField(db_column="id", primary_key=True, unique=True, null=False)

    clienteNombre = models.CharField(max_length=45, db_column="nombre", verbose_name="nombre", help_text="Ingresa aquí el nombre")

    clienteDocumento = models.CharField(max_length=12, db_column="documento", unique=True, verbose_name="documento")

    clienteDireccion = models.CharField(max_length=100, db_column="direccion", verbose_name="direccion")

    def __str__(self):
        return self.clienteNombre

    class Meta:
        db_table = "cliente"
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

class CabeceraModel(models.Model):   
    
    class opcionesTipo(models.TextChoices):
        VENTA = "V","VENTA"
        COMPRA = "C", "COMPRA"
        
    cabeceraId = models.AutoField(db_column="id", primary_key=True, unique=True, null=False)

    cabeceraFecha = models.DateTimeField(auto_now_add= True, db_column="fecha")

    cabeceraTipo = models.TextField(choices=opcionesTipo.choices, default=opcionesTipo.VENTA, db_column="tipo", null=False)

    #related_name Sirve para ingresar desde la clase clienteModel a todos sus registros de cabeceras
    clientes = models.ForeignKey(to=ClienteModel, db_column="clientes_id", null=False, related_name="clienteCabeceras", on_delete=models.PROTECT)

    class Meta:
        db_table = "cabecera_operaciones"
        verbose_name = "cabecera"
        verbose_name_plural = "cabeceras"

class DetalleModel(models.Model):

    detalleId = models.AutoField(db_column="id", primary_key=True, unique=True, null=False)

    detalleCantidad = models.IntegerField(db_column="cantidad", null=False)

    detalleImporte = models.DecimalField(db_column="importe", max_digits=5, decimal_places=2, null=False) 

    productos = models.ForeignKey(to="ProductoModel", db_column="productos_id", on_delete=models.PROTECT, related_name="productoDetalles", null=False)

    cabeceras = models.ForeignKey(to="CabeceraModel", db_column="cabecera_operaciones_id", on_delete=models.PROTECT, related_name="cabeceraDetalles", null=False)

    class Meta:
        db_table= "detalle_operaciones"
        verbose_name = "detalle"
        verbose_name_plural = "detalles"









