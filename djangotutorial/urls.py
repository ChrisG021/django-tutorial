"""
URL configuration for djangotutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    path('accounts/' , include("django.contrib.auth.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

################## api ###################################
from catalog.views import AuthorApiView, BookApiView, BookInstanceApiView, GenreApiView, LanguageApiView
urlpatterns += [
    path("api/book",BookApiView.as_view()),
    path("api/book/<int:pk>",BookApiView.as_view()),
    path("api/author", AuthorApiView.as_view()),
    path("api/author/<int:pk>", AuthorApiView.as_view()),
    path("api/bookinstance", BookInstanceApiView.as_view()),
    path("api/bookinstance/<str:pk>", BookInstanceApiView.as_view()),
    path("api/genre/", GenreApiView.as_view()),
    path("api/genre/<int:pk>/", GenreApiView.as_view()),
    path("api/language/", LanguageApiView.as_view()),
    path("api/language/<int:pk>/", LanguageApiView.as_view()),


]


############################################################

from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import path

