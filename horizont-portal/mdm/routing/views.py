from rest_framework import views
from .models import routing
from common.response import MdmResponse as Response

class RoutingView(views.APIView):

    def get(self, request, sale_username):
        return Response(data=routing[sale_username], status=200)
