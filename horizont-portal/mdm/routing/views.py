from rest_framework import permissions
from common.response import MdmResponse as Response
from rest_framework import generics, views
from common.permissions import is_backoffice
from common.views.class_based import BaseView

from . import models
from customer_store.models import CustomerStore

class RouteListView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_objects(self):
        return [
            {"id": str(route.id), "name": route.name, "stores": route.get_store_ids()}
            for route in models.Route.objects.all()
        ]

    def get(self, request):
        """
        This API support calling list of all route in the system.
        """
        routes = self.get_objects()
        return Response(routes, status=200)

    def post(self, request):
        """
        This API support to create route.
        """
        pass


class RouteView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
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

    def get(self, request, routename):
        """
        This API support to retrieve route detail.
        """
        pass

    def put(self, request, routename):
        """
        This API support to update route detail.
        """
        pass



class RouteCustomerStoreView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_route(self, route_id):
        try:
            return models.Route.objects.get(pk=route_id)
        except Exception as e:
            raise e

    def get_store(self, store_id):
        try:
            return CustomerStore.objects.get(pk=store_id)
        except Exception as e:
            raise e

    def put(self, request):
        """
        This API supports user or client to could attach/detach store from route.

        **param request:** None

        **return** {"success": true, "data": "Attach store to route complete."}
        """
        try:
            user = request.user
            data = request.data
            for route_id, store_ids in data.items():
                route = self.get_route(route_id)
                if store_ids:
                    for store_id in store_ids:
                        store = self.get_store(store_id)
                        if not models.RouteCustomerStore.objects.filter(route=route, store=store).exists():
                            models.RouteCustomerStore.objects.create(
                                store=store, route=route, status="CHECKIN"
                            )
                else:
                    models.RouteCustomerStore.objects.filter(route=route).delete()
            return Response("Attach store to route complete.", status=200)
        except Exception as e:
            return Response("Something went wrong.", status=500)



