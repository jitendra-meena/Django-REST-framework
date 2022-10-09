from django.contrib import admin
from django.urls import path
from .views import (
   ProjectList,
   List,
   Register,
   CompanyLogin,
   CompanyLogout,
   Developers,
   VerifyEmail,
   RequestPasswordResetEmail,
   PasswordTokenCheckAPI,
   SetNewPasswordAPIView
   )
   
urlpatterns = [
   path('projectlist/',ProjectList.as_view(),name="projectlist"),
   path('list/<int:manager_id>',List.as_view(),name="list"),
   path('register/',Register.as_view(),name="register"),
   path('company_login/',CompanyLogin.as_view(),name="company_login"),
   path('company_logout/',CompanyLogout.as_view(),name="company_logout"),
   path('developers/',Developers.as_view(),name="developers"),

   path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
   path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
   path('password-reset/<uidb64>/<token>/',
      PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
   path('password-reset-complete', SetNewPasswordAPIView.as_view(),
      name='password-reset-complete')

]


