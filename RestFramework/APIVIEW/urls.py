from django.contrib import admin
from django.urls import path
from .views import ProjectList, List
urlpatterns = [
   path('projectlist/',ProjectList.as_view(),name="projectlist"),
   path('list/<int:manager_id>',List.as_view(),name="list")
]