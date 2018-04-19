import django
from rest_framework import views
from rest_framework import permissions
from django.contrib.auth.models import User, Group

from common.response import MdmResponse as Response
from users.permissions import permissions as permission_permissions
from users.permissions import groups as group_permissions

true = True
false = False


class GrantRevokeUserToGroup(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        group_permissions.CouldGrantUserToGroup
    ]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise e

    def get_group(self, group_name):
        try:
            return Group.objects.get(name__istartswith=group_name)
        except Group.DoesNotExist as e:
            raise e

    def grants(self, userobj, groupobj):
        userobj.groups.add(groupobj)

    def revokes(self, userobj, groupobj):
        userobj.groups.remove(groupobj)

    def post(self, request, username, group_name):
        try:
            user = self.get_user(username)
            grp = self.get_group(group_name)
            self.grants(user, grp)
            data = "User has been grants to group."
            status = 200
        except User.DoesNotExist:
            data = "User Not Found."
            status = 204
        except Group.DoesNotExist:
            data = "Group (Role) Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def delete(self, request, username, group_name):
        try:
            user = self.get_user(username)
            grp = self.get_group(group_name)
            self.revokes(user, grp)
            data = "User has been revokes from group."
            status = 200
        except User.DoesNotExist:
            data = "User Not Found."
            status = 204
        except Group.DoesNotExist:
            data = "Group (Role) Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)