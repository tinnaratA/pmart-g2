from django.http import response
from django.shortcuts import render


from common.permissions import is_backoffice
from common.views.class_based import BaseView

from . import models

class RouteListView(BaseView):
    permissions = [
        is_backoffice
    ]

    def get_objects(self):
        return models.Route.objects.all()

    def set_contexts(self, **kwargs):
        return kwargs

    def get(self, request):
        if not self.check_permissions(request):
            return response.HttpResponseForbidden('You don\'t have permission(s) to perform this action.')
        routes = self.get_objects()
        contexts = self.set_contexts(routes=routes)
        return render(request, 'mdm/routing/main.html', contexts)


class RouteView(BaseView):
    permissions = [
        is_backoffice
    ]

    def get_objects(self, routename):
        return models.RouteActivity()
