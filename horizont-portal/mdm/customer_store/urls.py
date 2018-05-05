from django.urls import path

from . import views

urlpatterns = [
    path("store/list", views.CustomerStoreListView.as_view()),
]