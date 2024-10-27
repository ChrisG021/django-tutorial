from rest_framework import serializers
from catalog.models import Book,BookInstance,Author,Genre,Language

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title","author",'isbn','genre','language','summary')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name","last_name",'date_of_birth','date_of_death')