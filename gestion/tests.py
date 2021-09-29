from rest_framework.test import APITestCase
from .models import ProductoModel, ClienteModel

class ProductosTestCase(APITestCase):
    def setUp(self):
        ProductoModel(productoNombre="Teclado",productoPrecio=25.00,productoUnidadMedida="UN").save()
        ProductoModel(productoNombre="Mouse",productoPrecio=25.00,productoUnidadMedida="UN").save()
        ProductoModel(productoNombre="Parlantes",productoPrecio=25.00,productoUnidadMedida="UN").save()
        ProductoModel(productoNombre="WebCam",productoPrecio=25.00,productoUnidadMedida="UN").save()
        ProductoModel(productoNombre="Audifonos",productoPrecio=25.00,productoUnidadMedida="UN").save()

    def test_post_fail(self):
        #Deberia fallar el test cuando no le pasamos informacion
        request = self.client.post("/gestion/productos/")
        #print(request.status_code)
        #print(request.data)
        message=request.data.get("message")
        self.assertEqual(request.status_code,400)
        self.assertEqual(message,"Error al guardar el producto")
    
    def test_post_success(self):
        #Deberia retornar el producto creado
        #print(self.shortDescription)
        request = self.client.post("/gestion/productos/", data={
            "productoNombre": "Cartulina Canson Blanca",
            "productoPrecio": "0.50",
            "productoUnidadMedida": "UN"    
        }, format="json")
        message = request.data.get("message")

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, "Producto creado exitosamente")

    def test_get_success(self):
        #producto_encontrado = ProductoModel.objects.all()
        #print(producto_encontrado)
        request = self.client.get("/gestion/productos/?pagina=1&cantidad=2")
        
        #print(request.data)
        paginacion = request.data.get("paginacion")
        content = request.data.get("data").get("content")
        self.assertIsNone(paginacion.get("paginaPrevia"))
        self.assertIsNotNone(paginacion.get("paginaContinua"))
        self.assertEqual(paginacion.get("porPagina"), 2)
        self.assertEqual(len(content), 2)
        
class ClienteTestCase(APITestCase):
    def setUp(self):
        ClienteModel(clienteNombre="Cliente 001", clienteDocumento="03214567", clienteDireccion="Direccion 001", clienteEstado=True).save()
        ClienteModel(clienteNombre="Cliente 002", clienteDocumento="98765432", clienteDireccion="Direccion 002", clienteEstado=True).save()
        ClienteModel(clienteNombre="Cliente 003", clienteDocumento="74125896", clienteDireccion="Direccion 003", clienteEstado=True).save()
        ClienteModel(clienteNombre="Cliente 004", clienteDocumento="15975382", clienteDireccion="Direccion 004", clienteEstado=True).save()

    def test_post_fail(self):
        #Deberia fallar el test cuando no le pasamos informacion
        request = self.client.post("/gestion/clientes/")
        message=request.data.get("message")
        self.assertEqual(request.status_code,400)
        self.assertEqual(message,"Error al ingresar el cliente")

    def test_post_fail_falta_direccion(self):
        #Deberia fallar el test cuando no le pasamos direccion
        request = self.client.post("/gestion/clientes/", data={
            "clienteDocumento":"02898411"
        }, format="json")
        message=request.data.get("message")
        self.assertEqual(request.status_code,400)
        self.assertEqual(message,"Los clientes con DNI deben proveer la direccion")

    def test_post_fail_DNI_invalido(self):
        #Deberia fallar el test cuando pasamos un dni invalido
        request = self.client.post("/gestion/clientes/", data={
            "clienteDocumento":"99999999",
            "clienteDireccion":"Piura 963"
        }, format="json")
        message=request.data.get("message")
        self.assertEqual(request.status_code,400)
        self.assertEqual(message,"Documento incorrecto")

    def test_post_success(self):
        #Deberia retornar el cliente creado        
        request = self.client.post("/gestion/clientes/", data={
            "clienteDocumento":"02898411",
            "clienteDireccion":"Piura 567"
        }, format="json")
        message = request.data.get("message")

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, "Cliente agregado exitosamente")

    def test_get_fail(self):
        #Falla si no enviaos parametros de busqueda        
        request = self.client.get("/gestion/buscar-cliente/")
        message = request.data.get("message")
        self.assertEqual(request.status_code, 404)
        self.assertEqual(message, "Debe de ingresar nombre y/o documento del cliente a buscar")
    
    def test_get_success_nombre(self):
        #Busca cliente por nombre
        request = self.client.get("/gestion/buscar-cliente/?nombre=cliente")                
        content = request.data.get("content")
        self.assertEqual(len(content), 4)
        self.assertEqual(content[0].get("clienteNombre"), "Cliente 001")

    def test_get_success_documento(self):
        #Busca cliente por documento
        request = self.client.get("/gestion/buscar-cliente/?documento=74125896")                
        content = request.data.get("content")
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get("clienteNombre"), "Cliente 003")

        

    
