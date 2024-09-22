from rest_framework import serializers
from .models import Book, User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'available', 'return_date']

class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'borrowed_books']