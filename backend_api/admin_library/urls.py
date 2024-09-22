from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('users/borrowed-books/', UserViewSet.as_view({'get': 'borrowed_books'}), name='user-borrowed-books'),
    path('books/unavailable/', BookViewSet.as_view({'get': 'unavailable_books'}), name='book-unavailable'),
]