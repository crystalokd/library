from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import UserViewSet, BookViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]