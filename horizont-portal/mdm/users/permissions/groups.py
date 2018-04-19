from rest_framework import permissions


class CouldListGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_user = request.user
        if auth_user.is_superuser:
            return True

        if 'back_officer' in [grp.name.replace(' ', '_').lower() for grp in auth_user.groups.all()]:
            return True
        return False


class CouldActionGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_user = request.user
        if auth_user.is_superuser:
            return True

        perms = [perm.codename for grp in auth_user.groups.all() for perm in grp.permissions.all()]
        groups = [grp.name.replace(' ', '_').lower() for grp in auth_user.groups.all()]

        if 'back_officer' in groups:
            if request.method == "DELETE" and 'delete_group' in perms:
                return True
            elif request.method == "GET":
                return True
            elif request.method == "POST" and 'add_group' in perms:
                return True
            elif request.method == "PUT" and 'change_group' in perms:
                return True
            else:
                return True
        return False


class CouldGrantUserToGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_user = request.user
        if auth_user.is_superuser:
            return True

        perms = [perm.codename for grp in auth_user.groups.all() for perm in grp.permissions.all()]
        groups = [grp.name.replace(' ', '_').lower() for grp in auth_user.groups.all()]
        if 'back_officer' in groups:
            if request.method == "POST" and 'change_user' in perms:
                return True
            elif request.method == "DELETE" and 'change_user' in perms:
                return True
            else:
                return False
        return False
