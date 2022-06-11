from django.contrib import admin
from django.urls import path
from .views import ProjectList, List,Register,CompanyLogin, CompanyLogout,VerifyEmail

urlpatterns = [
   path('projectlist/',ProjectList.as_view(),name="projectlist"),
   path('list/<int:manager_id>',List.as_view(),name="list"),
   path('register/',Register.as_view(),name="register"),
   path('company_login/',CompanyLogin.as_view(),name="company_login"),
   path('company_logout/',CompanyLogout.as_view(),name="company_logout"),
   path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]


