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
from catalog.views import BookApiView
urlpatterns += [
    path("api/book",BookApiView.as_view()),
    path("api/book/<int:pk>",BookApiView.as_view()),
]


############################################################

from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import path

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

urlpatterns += [
    path('accounts/logout/', custom_logout, name='logout'),
]