from rest_framework import views
from .models import routing
from common.response import MdmResponse as Response

class RoutingView(views.APIView):

    def get(self, request, sale):
        return Response(data=routing[sale], status=200)
