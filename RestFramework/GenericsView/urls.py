from django.contrib import admin
from django.urls import path
from .views import Developer, UpdateDeveloper

urlpatterns = [
    path('developer/',Developer.as_view(),name="developer_list"),
    path('update_developer/<int:id>',UpdateDeveloper.as_view(),name="update_developer")
]