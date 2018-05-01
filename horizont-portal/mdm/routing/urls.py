from django.urls import path

from . import views

urlpatterns = [
    path('route/list', views.RouteListView.as_view())
]