from django.contrib import admin
from catalog.models import Book,BookInstance,Author,Genre,Language
# Register your models here.
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
#parte do tabular inline eu n saquei
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(Author)   
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    #em formato de tupla ele organiza horizontalmente

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ("id", "name",)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        #coloca um nome em realce no admin
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
