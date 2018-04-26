from django.urls import path

from .views import CustomerStoreView, CustomerListView, CreateCustomerStoreView

urlpatterns = [
    path('store/list', CustomerListView.as_view()),
    path('store', CreateCustomerStoreView.as_view()),
    path('store/<store_name>', CustomerStoreView.as_view()),
    # path('store/<store_name>/orders', CustomerOrderView.as_view())
]