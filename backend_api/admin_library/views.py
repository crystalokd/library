from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, User
from .serializers import BookSerializer, UserSerializer
import pika
import json


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
import requests



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # def perform_create(self, serializer):
    #     book = serializer.save()
    #     self.publish_book_update(book, 'create')

    # def perform_update(self, serializer):
    #     book = serializer.save()
    #     self.publish_book_update(book, 'update')

    # def perform_destroy(self, instance):
    #     self.publish_book_update(instance, 'delete')
    #     instance.delete()

    # def publish_book_update(self, book, action):
    #     print("-----------------------------------")
    #     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

    #     channel = connection.channel()
    #     channel.queue_declare(queue='book_updates')
        
    #     message = {
    #         'action': action,
    #         'book': BookSerializer(book).data
    #     }
        
    #     channel.basic_publish(exchange='',
    #                           routing_key='book_updates',
    #                           body=json.dumps(message))
    #     connection.close()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def borrowed_books(self, request):
        users = User.objects.filter(borrowed_books__isnull=False)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unavailable_books(self, request):
        books = Book.objects.filter(available=False)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)






FRONTEND_API_URL = 'http://127.0.0.1:8001/api/books/'  # Replace with your frontend API URL

@receiver(post_save, sender=Book)
def notify_frontend_api(sender, instance, created, **kwargs):
    """
    Signal to notify the frontend API whenever a new book is added to the catalogue.
    """
    if created:
        # Book was just created
        book_data = {
            'title': instance.title,
            'author': instance.author,
            'publisher': instance.publisher,
            'category': instance.category,
        }

        # Send the data to the frontend API
        try:
            response = requests.post(FRONTEND_API_URL, json=book_data)
            response.raise_for_status()  # Raise error for bad responses
        except requests.exceptions.RequestException as e:
            # Handle any error that occurs when communicating with the frontend API
            print(f"Error notifying frontend API: {e}")
