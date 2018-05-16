import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import generics, views
from rest_framework import parsers
from common.response import MdmResponse as Response

from . import models
from .serializers import CustomerStoreSerializer

class CustomerStoreTypeListView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        storetypes = [
            {
                "code": typ.code,
                "name": typ.name,
                "children": {subtyp.code: subtyp.name for subtyp in typ.get_children()}
            }
            for typ in models.CustomerStoreType.objects.filter(parent=None)
        ]
        return Response(storetypes, status=200)


class CustomerStoreListView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_objects(self):
        return models.CustomerStore.objects.all()

    def get(self, request):
        stores = self.get_objects()
        serializer = CustomerStoreSerializer(stores, many=True)
        return Response(serializer.data, status=200)


class CustomerStoreView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_objects(self, id):
        try:
            return models.CustomerStore.objects.get(pk=id)
        except models.CustomerStore.DoesNotExist as e:
            raise e

    def get(self, request, id):
        try:
            store = self.get_objects(id)
            serializer = CustomerStoreSerializer(store, many=False)
            return Response(serializer.data, status=200)
        except models.CustomerStore.DoesNotExist as e:
            return Response("No record", status=204)


class CustomerStoreCreateView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        try:
            data = [request.data] if not isinstance(request.data, (tuple, list)) else request.data
            serializer = CustomerStoreSerializer(data=data, many=True)
            if serializer.is_valid():
                print(serializer.save())
                return Response("Customer store has been created.", status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response("Something went wrong.", status=500)


class CustomerStoreImageView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_store(self, id):
        try:
            return models.CustomerStore.objects.get(pk=id)
        except models.CustomerStore.DoesNotExist as e:
            raise e

    def get(self, request, id):
        try:
            images = models.CustomerStoreImage.objects.filter(customer_store=self.get_store(id))
            content_returned = [img.url for img in images]
            return Response(content_returned, status=200)
        except models.CustomerStoreImage.DoesNotExist as e:
            return Response("The store no have image.", status=204)
        except models.CustomerStore.DoesNotExist:
            return Response("Store not found.", status=204)
        except Exception as e:
            return Response("Something went wrong.", status=500)

    def post(self, request, id):
        try:
            file = request.data.get('file')
            content = file.read()
            filepath = os.path.join(settings.MEDIA_ROOT, 'images', 'customer_store', id + '.png')
            fp = open(filepath, mode="wb")
            fp.write(content)
            fp.close()
            models.CustomerStoreImage.objects.create(customer_store=self.get_store(id), abspath=filepath)
        except models.CustomerStore.DoesNotExist:
            return Response("Store not found.", status=204)
        except Exception as e:
            return Response("Something went wrong.", status=500)
        return Response("Image has been uploaded.", status=201)
