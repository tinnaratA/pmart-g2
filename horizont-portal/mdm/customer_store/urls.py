from django.urls import path

from . import views

urlpatterns = [
    path("store/type/list", views.CustomerStoreTypeListView.as_view()),

    path("store/list", views.CustomerStoreListView.as_view()),
]