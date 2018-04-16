from rest_framework import permissions
from django.contrib.auth.models import User

class CouldActionUserProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        method = request.method
        auth_user = request.user
        if auth_user.is_superuser:
            return True

        # check username argument
        kwargs_keys = view.kwargs.keys()
        if 'username' not in kwargs_keys:
            username = auth_user.username
        else:
            username = view.kwargs.get('username')

        # Check permissions
        groups = auth_user.groups.all()
        perms = [perm.codename for grp in groups for perm in grp.permissions.all()]
        if 'add_user' in perms and method == "POST":
            return True
        elif method == "GET" and username == auth_user.username:
            return True
        elif ('change_user' in perms and method == "PUT") or (username == auth_user.username):
            try:
                # Check normal user change admin profile
                queryuser = User.objects.get(username=username)
                if queryuser.is_superuser:
                    return False
                return True
            except User.DoesNotExist as e:
                return False
        return False


class CouldListUserProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_user = request.user
        if auth_user.is_superuser:
            return True

        if 'back_officer' in [grp.name.replace(' ', '_').lower() for grp in auth_user.groups.all()]:
            return True
        return False
