from django.urls import path

from . import views

urlpatterns = [
    # Instance
    path('list', views.ListUserView.as_view()),
    path('profile', views.UserView.as_view()),
    path('profile/<username>', views.UserView.as_view()),
    path('<username>/delete', views.DeleteUserView.as_view()),

    # Role
    # path('role/create'),
    # path('role/<role_name>/edit')
    # path('role/<role_name>/delete'),

    # Grant

]
