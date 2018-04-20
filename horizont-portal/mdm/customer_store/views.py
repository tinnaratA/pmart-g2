from rest_framework import generics, views
from common.response import MdmResponse as Response
from .models import stores
from .models import orders


class CustomerStoreView(views.APIView):

    def get(self, request, store_name):
        return Response(data=list(filter(lambda x: x['name'] == store_name, stores)), status=200)


class CustomerOrderView(views.APIView):

    def get(self, request, store_name):
        data = [d['order_list'] for d in list(filter(lambda x: x['store']['name'] == store_name, orders))]
        return Response(data=data, status=200)
