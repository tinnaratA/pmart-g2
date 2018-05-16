from django.urls import path

from . import views

urlpatterns = [
    path('route/list', views.RouteListView.as_view()),
    path('route/name/<routename>', views.RouteView.as_view()),
    path('route/attach/stores', views.RouteCustomerStoreView.as_view()),
]