from django.urls import path

from . import views

urlpatterns = [
    path("store/create", views.CustomerStoreCreateView.as_view()),
    path("store/type/list", views.CustomerStoreTypeListView.as_view()),
    path("store/list", views.CustomerStoreListView.as_view()),
    path("store/image/<id>", views.CustomerStoreImageView.as_view()),
    path("store/<id>", views.CustomerStoreView.as_view()),
]