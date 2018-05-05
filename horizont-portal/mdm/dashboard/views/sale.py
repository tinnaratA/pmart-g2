from rest_framework import permissions
from rest_framework.response import Response as JsonResponse
from rest_framework import generics, views

from routing import models as route_models


class SaleDashBoard(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def set_contexts(self, **kwargs):
        return kwargs

    def get_user_roles(self, user):
        return [grp.name for grp in user.groups.all()]

    def get_objects(self, user):
        if 'back_office' in self.get_user_roles(user) or user.is_superuser:
            return [
                # {
                #     "store": task.activity.route_stores.store.to_dict(),
                #     "status": task.activity.route_stores.status
                # }
                task.activity.route_stores.to_dict()
                for task in route_models.RouteActivityTask.objects.all()
            ]
        elif 'canvas' in self.get_user_roles(user):
            return [
                # {
                #     "store": task.activity.route_stores.store.to_dict(),
                #     "status": task.activity.route_stores.status
                # }
                task.activity.route_stores.to_dict()
                for task in route_models.RouteActivityTask.objects.filter(executed_by=user)
            ]
        else:
            raise PermissionError

    def get(self, request):
        try:
            user = request.user
            tasks = self.get_objects(user)
            contexts = self.set_contexts(tasks=tasks)
            return JsonResponse(contexts, status=200)
        except PermissionError as e:
            return JsonResponse({"detail": "You don't have permissions to perform this action."}, status=403)

