from django.urls import path

from .views import users as user_views
from .views import groups as group_views
from .views import permissions as permission_views
from .views import grants_revokes as grant_revoke_views

urlpatterns = [
    # user
    path('users/list', user_views.ListUserView.as_view()),
    path('users/profile', user_views.UserView.as_view()),
    path('users/profile/<username>', user_views.UserView.as_view()),
    path('users/profile/<username>/delete', user_views.DeleteUserView.as_view()),

    # group (role)
    path('groups/list', group_views.ListGroupView.as_view()),
    path('groups', group_views.GroupView.as_view()),
    path('groups/<group_name>', group_views.GroupView.as_view()),

    # permission
    path('permissions/list', permission_views.ListPermissionView.as_view()),
    path('permissions', permission_views.PermissionView.as_view()),
    path('permissions/<perm_code>', permission_views.PermissionView.as_view()),

    #
    #   grant/revoke group (role) & permission
    #     - POST method to grants
    #     - DELETE method to revokes
    #

    path('grants/user/<username>/group/<group_name>', grant_revoke_views.GrantRevokeUserToGroup.as_view()),
    path('grants/permission/<perm_code>/group/<group_name>', grant_revoke_views.GrantRevokePermissionToGroup.as_view()),
    path('grants/permission/<perm_code>/user/<username>', grant_revoke_views.GrantRevokePermissionToUser.as_view()),
]
