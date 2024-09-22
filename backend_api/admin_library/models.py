from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    return_date = models.DateTimeField(null=True, blank=True)

class User(models.Model):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    borrowed_books = models.OneToOneField('Book', on_delete=models.SET_NULL, null=True, blank=True)
