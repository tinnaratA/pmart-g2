from django.contrib.auth.models import Permission
from rest_framework import generics, views
from rest_framework import permissions
from rest_framework import pagination

from common.response import MdmResponse as Response
from users.permissions import permissions as permission_permissions
from users.serializers.permissions import PermissionSerializer

true = True
false = False


class ListPermissionView(generics.ListAPIView):
    """
            Show list of permission API
    """
    queryset = Permission.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permission_permissions.CouldListPermission
    ]
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return Response(data=response.data, status=200)


class PermissionView(views.APIView):
    """
            CRUD permission APIs
            * GET method as retrieve
            * POST method as create
            * PUT method as update
            * DELETE method as remove
    """
    permission_classes = [
        permissions.IsAuthenticated,
        permission_permissions.CouldActionPermission
    ]

    def get_objects(self, perm_code):
        try:
            return Permission.objects.get(codename__istartswith=perm_code.lower())
        except Permission.DoesNotExist as e:
            raise e
        except Exception as e:
            raise e

    def get(self, request, perm_code=None):
        try:
            perm = self.get_objects(perm_code)
            serializer = PermissionSerializer(perm, many=False)
            data = serializer.data
            status = 200
        except Permission.DoesNotExist as e:
            data = "Permission Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def post(self, request):
        try:
            data = request.data
            if not isinstance(data, (tuple, list)):
                data = [data]

            serializer = PermissionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                data = "Permission has been created."
                status = 200
            else:
                data = serializer.errors
                status = 400
        except Permission.DoesNotExist as e:
            data = "Permission Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def put(self, request, perm_code=None):
        try:
            partial_flag = eval(request.GET.get('partial', 'false'))
            perm = self.get_objects(perm_code)
            serializer = PermissionSerializer(perm, data=request.data,  partial=partial_flag)
            if serializer.is_valid():
                serializer.update(serializer.instance, serializer.validated_data)
                data = "Permission has been updated."
                status = 200
            else:
                data = serializer.errors
                status = 400
        except Permission.DoesNotExist as e:
            data = "Permission Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
            raise e
        finally:
            return Response(data=data, status=status)

    def delete(self, request, perm_code=None):
        try:
            perm = self.get_objects(perm_code)
            perm.delete()
            data = "Permission has been deleted."
            status = 200
        except Permission.DoesNotExist as e:
            data = "Permission Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)
