from rest_framework import permissions
from rest_framework.response import Response as JsonResponse
from rest_framework import generics, views
from common.permissions import is_backoffice
from common.views.class_based import BaseView

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