from django.urls import path

from .views import users as user_views
from .views import groups as group_views
from .views import permissions as permission_views

urlpatterns = [
    # user
    path('list', user_views.ListUserView.as_view()),
    path('profile', user_views.UserView.as_view()),
    path('profile/<username>', user_views.UserView.as_view()),
    path('profile/<username>/delete', user_views.DeleteUserView.as_view()),

    # group (role)
    path('group/list', group_views.ListGroupView.as_view()),
    path('group', group_views.GroupView.as_view()),
    path('group/<group_name>', group_views.GroupView.as_view()),

    # permission
    path('permission/list', permission_views.ListPermissionView.as_view()),
    path('permission', permission_views.PermissionView.as_view()),
    path('permission/<perm_code>', permission_views.PermissionView.as_view()),

    # grant group (role) & permission
    # path('grant/group/<group_name>/user/<username>'),
    # path('grant/user/<username>/group/<group_name>'),
    # path('grant/permission/<perm_code>/group/<group_name>'),
    # path('grant/permission/<perm_code>/user/<username>'),

    # revoke group (role) & permission
    # path('revoke/group/<group_name>/user/<username>'),
    # path('revoke/user/<username>/group/<group_name>'),
    # path('revoke/permission/<perm_code>/group/<group_name>'),
    # path('revoke/permission/<perm_code>/user/<username>'),
]
