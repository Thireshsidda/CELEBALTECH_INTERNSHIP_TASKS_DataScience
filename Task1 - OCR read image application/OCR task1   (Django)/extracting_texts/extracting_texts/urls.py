"""extracting_texts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from word_extracter import views

urlpatterns = [
    path('', views.home, name='home'),
    path('extract/url', views.extract_from_url, name='extract_from_url'),
    path('extract/file', views.extract_from_file, name='extract_from_file'),
    path('extract/folder', views.extract_from_folder, name='extract_from_folder'),
]

