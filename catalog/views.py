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

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


########################################################### rest api ######################################

from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models

class BookApiView(APIView):
    def get(self, request,pk=None):
        if pk:
            book = Book.objects.get(pk=pk)
            toJson = serializers.BookSerializer(book)
        else:
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

class AuthorApiView(APIView):
    def get(self, request,pk=None):
        if pk:
            author = self.get_object(pk)
            toJson = serializers.AuthorSerializer(author)
        else:
            author = models.Author.objects.all()
            toJson = serializers.AuthorSerializer(author, many =True) #many pra lidar com mts dados
        return Response(toJson.data, status=200)
    
    def post(self, request):
        serializer = serializers.AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        Author = self.get_object(pk)
        serializer = serializers.AuthorSerializer(Author, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk): 
        author = self.get_object(pk)
        author.delete()
        return Response(status=204)

class BookInstanceApiView(APIView):
    def get(self, request,pk=None):
        if pk:
            bookinstance = self.get_object(pk)
            toJson = serializers.BookInstanceSerializer(bookinstance)
        else:
            bookinstance = models.BookInstance.objects.all()
            toJson = serializers.BookInstanceSerializer(bookinstance, many =True) #many pra lidar com mts dados
        return Response(toJson.data, status=200)
    
    def post(self, request):
        serializer = serializers.BookInstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    def get_object(self, pk):
        try:
            return BookInstance.objects.get(pk=pk)
        except BookInstance.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        bookInstance = self.get_object(pk)
        serializer = serializers.BookInstanceSerializer(bookInstance, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk): 
        bookInstance = self.get_object(pk)
        bookInstance.delete()
        return Response(status=204)

class GenreApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            genre = self.get_object(pk)
            serializer = serializers.GenreSerializer(genre)
        else:
            genres = models.Genre.objects.all()
            serializer = serializers.GenreSerializer(genres, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = serializers.GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def get_object(self, pk):
        try:
            return models.Genre.objects.get(pk=pk)
        except models.Genre.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        genre = self.get_object(pk)
        serializer = serializers.GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        genre = self.get_object(pk)
        genre.delete()
        return Response(status=204)

class LanguageApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            language = self.get_object(pk)
            serializer = serializers.LanguageSerializer(language)
        else:
            languages = models.Language.objects.all()
            serializer = serializers.LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = serializers.LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def get_object(self, pk):
        try:
            return models.Language.objects.get(pk=pk)
        except models.Language.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        language = self.get_object(pk)
        serializer = serializers.LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        language = self.get_object(pk)
        language.delete()
        return Response(status=204)
