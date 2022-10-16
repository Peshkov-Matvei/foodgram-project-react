from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
