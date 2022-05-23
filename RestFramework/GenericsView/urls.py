from django.contrib import admin
from django.urls import path
from .views import Developer, UpdateManager

urlpatterns = [
    path('developer/',Developer.as_view(),name="developer_list"),
    path('update_manager/<int:pk>',UpdateManager.as_view(),name="update_manager")
]