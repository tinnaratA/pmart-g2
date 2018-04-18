from django.contrib.auth.models import Group
from rest_framework import generics, views
from rest_framework import permissions
from rest_framework import pagination

from common.response import MdmResponse as Response
from users.permissions import groups as group_permissions
from users.serializers.groups import GroupSerializer

true = True
false = False


class ListGroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        group_permissions.CouldListGroup
    ]
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return Response(data=response.data, status=200)


class GroupView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        group_permissions.CouldActionGroup
    ]

    def get_objects(self, group_name):
        try:
            return Group.objects.get(name__istartswith=group_name.lower())
        except Group.DoesNotExist as e:
            raise e
        except Exception as e:
            raise e

    def get(self, request, group_name=None):
        try:
            grp = self.get_objects(group_name)
            serializer = GroupSerializer(grp, many=False)
            data = serializer.data
            status = 200
        except Group.DoesNotExist as e:
            data = "Group (Role) Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def put(self, request, group_name=None):
        try:
            grp = self.get_objects(group_name)
            serializer = GroupSerializer(grp, data=request.data)
            if serializer.is_valid():
                serializer.update(serializer.instance, serializer.validated_data)
                data = "Group (Role) has been updated."
                status = 200
            else:
                data = serializer.errors
                status = 400
        except Group.DoesNotExist as e:
            data = "Group (Role) Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def post(self, request, group_name=None):
        try:
            data = request.data
            if not isinstance(data, (tuple, list)):
                data = [data]

            serializer = GroupSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                data = "Group (Role) has been created."
                status = 201
            else:
                data = serializer.errors
                status = 400
        except Group.DoesNotExist as e:
            data = "Group (Role) Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def delete(self, request, group_name=None):
        try:
            grp = self.get_objects(group_name)
            grp.delete()
            data = "Group (Role) has been deleted."
            status = 200
        except Group.DoesNotExist as e:
            data = "Group (Role) Not Found."
            status = 204
        except Exception as e:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

