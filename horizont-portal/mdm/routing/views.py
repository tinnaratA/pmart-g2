from rest_framework import permissions
from rest_framework.response import Response as JsonResponse
from rest_framework import generics, views
from common.permissions import is_backoffice
from common.views.class_based import BaseView

from . import models

class RouteListView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_objects(self):
        return [
            {"id": str(route.id), "name": route.name, "stores": route.get_store_ids()}
            for route in models.Route.objects.all()
        ]

    def set_contexts(self, **kwargs):
        return kwargs

    def get(self, request):
        routes = self.get_objects()
        contexts = self.set_contexts(routes=routes)
        return JsonResponse(contexts, status=200)


class RouteView(BaseView):
    permissions = [
        is_backoffice
    ]

    def get_objects(self, routename):
        try:
            route = models.Route.objects.get(name__iexact=routename)
        except models.Route.MultipleObjectsReturned as e:
            try:
                route = models.Route.objects.filter(name__iexact=routename)[0]
                return route
            except IndexError as e:
                raise e
        except models.Route.DoesNotExist("No record.") as e:
            raise e

    # def get(self, request, routename):
    #     try:
    #         route = self.get_objects(routename)
    #     except IndexError:
    #
    #     return
