from django.urls import path

from .views import CustomerStoreView, CustomerOrderView

urlpatterns = [
    path('store/<store_name>', CustomerStoreView.as_view()),
    # path('store/<store_name>/orders', CustomerOrderView.as_view())
]