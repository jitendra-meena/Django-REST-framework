from django.contrib import admin
from django.urls import path
from .views import developers, UpdateManager

urlpatterns = [
    path('developers/',developers,name="developers_list")
]