"""mdm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from users.urls import urlpatterns as users_urls
from customer_store.urls import urlpatterns as customer_store_urls
from routing.urls import urlpatterns as routing_urls
from dashboard.urls import urlpatterns as dashboard_urls

from users.views import authentication

schema_view = get_swagger_view(title='Master Data Management API')

urlpatterns = [
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('authentication', authentication.Authentication.as_view()),
    path('deauthentication', authentication.Deauthentication.as_view()),

    path('admin/', admin.site.urls),
    path('users/mdm/', include((users_urls, 'users'), namespace='users_api')),

    path('customers/', include((customer_store_urls, 'customer_store'), namespace='customers_api')),
    path('dashboard/', include((dashboard_urls, 'dashboard'), namespace='dashboard_api')),
    path('routing/', include((routing_urls, 'routing'), namespace='routing_api')),

    # Landing Page Place Holder with API Docs
    path('', include_docs_urls(title='Master Data Management API')),
    path('docs/', include_docs_urls(title='Master Data Management API')),
    path('docs/swagger', schema_view),

    # path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
