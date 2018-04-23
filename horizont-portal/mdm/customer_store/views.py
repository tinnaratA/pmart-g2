from rest_framework import generics, views
from rest_framework import permissions
from rest_framework import pagination

from common.response import MdmResponse as Response

from . import models

from .serializers import CustomerStoreSerializer


class CustomerListView(generics.ListAPIView):
    queryset = models.CustomerStore.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = CustomerStoreSerializer

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return Response(data=response.data, status=200)


class CustomerStoreView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_objects(self, store_name):
        try:
            return models.CustomerStore.objects.get(store_name__iexact=store_name)
        except models.CustomerStore.DoesNotExist as e:
            raise e

    def get(self, request, store_name):
        try:
            store = self.get_objects(store_name)
            serializer = CustomerStoreSerializer(store, many=False)
            data = serializer.data
            status = 200
        except models.CustomerStore.DoesNotExist:
            data = "Customer store Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong"
            status = 500
        finally:
            return Response(data=data, status=status)


class CustomerOrderView(views.APIView):

    def get(self, request, store_name):
        data = [d['order_list'] for d in list(filter(lambda x: x['store']['name'] == store_name, orders))]
        return Response(data=data, status=200)
