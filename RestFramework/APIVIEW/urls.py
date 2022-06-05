from django.contrib import admin
from django.urls import path
from .views import ProjectList, List,Register,CompanyLogin

urlpatterns = [
   path('projectlist/',ProjectList.as_view(),name="projectlist"),
   path('list/<int:manager_id>',List.as_view(),name="list"),
   path('register/',Register.as_view(),name="register"),
   path('company_login/',CompanyLogin.as_view(),name="company_login")
]


