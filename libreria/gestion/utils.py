from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginacionPersonalizada(PageNumberPagination):
    # nombre de la variable para indicar el número de pagina
    page_query_param = 'pagina'
    # page el tyamaño de los items por pagina por defecto
    page_size = 2
    # page_size_query_paramel nombre del avariable que usaremos para indicar la cantidad elementos por pagina
    page_size_query_param = "cantidad"
    # max_page_size sirve para limitar el tamaño de pagina
    max_page_size = 10

    def get_paginated_response(self, data):
        # data informacion que esta siendo paginada
        return Response(data={
            "paginacion":{
                "paginaContinua": self.get_next_link(),
                "paginaPrevia": self.get_previous_link(),
                "total":self.page.paginator.count,                
                "porPagina":self.page.paginator.per_page
            },
            "data": {"content": data, "message": None}})
