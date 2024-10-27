from django.http import Http404
from django.shortcuts import render
from catalog.models import Book,Author,BookInstance,Genre
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status='a').count()

    #all impcito por padrao
    num_authors = Author.objects.count()

    num_visits = request.session.get("num_visits", 0)
    num_visits+=1

    request.session["num_visits"] = num_visits
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)

################ views ###########################
from django.views import generic

class BookListView(generic.ListView) :
    model = Book
    """É isso aí! A view genérica consultará o banco de dados para obter todos os registros para o modelo especificado (Book) em seguida, renderize um template localizado em /locallibrary/catalog/templates/catalog/book_list.html"""
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
def author_detail_view(request,pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        raise Http404('author does not exist')
    return render(request, "catalog/author_detail.html", 
                  context={'author':author, 'book_list': Book.objects.filter(author=author)})
##sou um genio eu utilizei a função pra gerar a pagina e coloquei no contexto ambos os objteos necessarios


########################################################### rest api ######################################

from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models

class BookApiView(APIView):
    def get(self, request):
        book = models.Book.objects.all()
        toJson = serializers.BookSerializer(book, many =True) #many pra lidar com mts dados

        return Response(toJson.data)
    
    def post(self, request):
        serializer = serializers.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = serializers.BookSerializer(book, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk): 
        book = self.get_object(pk)
        book.delete()
        return Response(status=201) 