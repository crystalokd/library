# frontend_api/frontend_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),  # Include the URLs from the library app
]