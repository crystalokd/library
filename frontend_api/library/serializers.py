from rest_framework import serializers
from .models import User, Book, Borrowing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'available', 'return_date']

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['id', 'user', 'book', 'borrow_date', 'return_date']
