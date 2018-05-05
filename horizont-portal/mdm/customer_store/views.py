from rest_framework import permissions
from rest_framework.response import Response as JsonResponse
from rest_framework import generics, views
from django.db.models import Q

from . import models


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
        return JsonResponse(storetypes, status=200)


class CustomerStoreListView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def set_contexts(self, **kwargs):
        return kwargs

    def get_objects(self):
        return [cs.to_dict() for cs in models.CustomerStore.objects.all()]

    def get(self, request):
        stores = self.get_objects()
        contexts = self.set_contexts(stores=stores)
        return JsonResponse(stores, status=200)


class CustomerStoreView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def set_contexts(self, **kwargs):
        return kwargs

    def get_objects(self, id):
        try:
            return models.CustomerStore.objects.get(pk=id)
        except models.CustomerStore.DoesNotExist as e:
            raise e

    def get(self, request, id):
        try:
            store = self.get_objects(id)
            return JsonResponse(store.to_dict(), status=200)
        except models.CustomerStore.DoesNotExist as e:
            return JsonResponse({'detail': 'No record'}, status=204)
