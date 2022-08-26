from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Blogs.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
