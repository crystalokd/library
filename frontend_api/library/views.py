from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Book, Borrowing
from .serializers import UserSerializer, BookSerializer, BorrowingSerializer
from django.utils import timezone
from datetime import timedelta

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        publisher = self.request.query_params.get('publisher')
        category = self.request.query_params.get('category')
        
        if publisher:
            queryset = queryset.filter(publisher=publisher)
        if category:
            queryset = queryset.filter(category=category)
            
        
        return queryset

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if not book.available:
            return Response({"error": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST)

        days = int(request.data.get('days', 14))
        user_id = request.data.get('user_id')
        print(user_id, "gblrbvjkbv>>>>>>>.")
        
        # try:
        #     user = User.objects.get(id=user_id)
        # except User.DoesNotExist:
        #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return_date = timezone.now() + timedelta(days=days)
        
        Borrowing.objects.create(book=book, return_date=return_date)
        book.available = False
        book.return_date = return_date
        book.save()

        return Response({"message": f"Book borrowed for {days} days"}, status=status.HTTP_200_OK)


