from django.urls import path

from . import views

urlpatterns = [
    path('route/list', views.RouteListView.as_view()),
    path('route/<routename>', views.RouteView.as_view())
]