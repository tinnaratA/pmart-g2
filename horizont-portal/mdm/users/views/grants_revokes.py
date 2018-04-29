import django
from rest_framework import views
from rest_framework import permissions
from django.contrib.auth.models import User, Group, Permission

from common.response import MdmResponse as Response
from users.permissions import permissions as permission_permissions
from users.permissions import groups as group_permissions

true = True
false = False


class GrantRevokeUserToGroup(views.APIView):
    """
        Grant/Revoke User to Group APIs
        are allowed user who are in the `back officer` group or have permissions to perform these actions.
        The actions are grants or revokes specific user from group (aka. role)
    """

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
            data = "Grant user to group has been successful."
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
            data = "Revoke user to group has been successful."
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


class GrantRevokePermissionToGroup(views.APIView):
    """
            Grant/Revoke Permission to Group APIs
            are allowed user who are in the `back officer` group or have permissions to perform these actions.
            The actions are grants or revokes specific permission from group (aka. role)
    """

    permission_classes = [
        permissions.IsAuthenticated,
        permission_permissions.CouldGrantPermissionToGroup
    ]

    def get_permission(self, perm_code):
        try:
            return Permission.objects.get(codename=perm_code)
        except Permission.DoesNotExist as e:
            raise e

    def get_group(self, group_name):
        try:
            return Group.objects.get(name__istartswith=group_name)
        except Group.DoesNotExist as e:
            raise e

    def grants(self, permobj, groupobj):
        permobj.group_set.add(groupobj)

    def revokes(self, permobj, groupobj):
        permobj.group_set.remove(groupobj)

    def post(self, request, perm_code, group_name):
        try:
            perm = self.get_permission(perm_code)
            grp = self.get_group(group_name)
            self.grants(perm, grp)
            data = "Grant permission to group has been successful."
            status = 200
        except Permission.DoesNotExist:
            data = "Permission Not Found."
            status = 204
        except Group.DoesNotExist:
            data = "Group (Role) Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def delete(self, request, perm_code, group_name):
        try:
            perm = self.get_permission(perm_code)
            grp = self.get_group(group_name)
            self.revokes(perm, grp)
            data = "Rovke permission to group has been successful."
            status = 200
        except Permission.DoesNotExist:
            data = "Permission Not Found."
            status = 204
        except Group.DoesNotExist:
            data = "Group (Role) Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)


class GrantRevokePermissionToUser(views.APIView):
    """
            Grant/Revoke Permission to User APIs
            are allowed user who are in the `back officer` group or have permissions to perform these actions.
            The actions are grants or revokes specific permission from user.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        permission_permissions.CouldGrantPermissionToGroup
    ]

    def get_permission(self, perm_code):
        try:
            return Permission.objects.get(codename=perm_code)
        except Permission.DoesNotExist as e:
            raise e

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise e

    def grants(self, permobj, userobj):
        permobj.user_set.add(userobj)

    def revokes(self, permobj, userobj):
        permobj.user_set.remove(userobj)

    def post(self, request, perm_code, username):
        try:
            perm = self.get_permission(perm_code)
            user = self.get_user(username)
            self.grants(perm, user)
            data = "Grant permission to user has been successful."
            status = 200
        except Permission.DoesNotExist:
            data = "Permission Not Found."
            status = 204
        except User.DoesNotExist:
            data = "User Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)

    def delete(self, request, perm_code, username):
        try:
            perm = self.get_permission(perm_code)
            user = self.get_user(username)
            self.revokes(perm, user)
            data = "Rovke permission to user has been successful."
            status = 200
        except Permission.DoesNotExist:
            data = "Permission Not Found."
            status = 204
        except User.DoesNotExist:
            data = "User Not Found."
            status = 204
        except Exception:
            data = "Something went wrong."
            status = 500
        finally:
            return Response(data=data, status=status)
