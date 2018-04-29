from django.urls import path

from .views import RoutingView

urlpatterns = [
    path('route/<sale_username>', RoutingView.as_view())
]