from django.urls import path,include
from rest_framework import routers
from .views import CompanyViewSet,CompanyVDataiewSet

routers = routers.DefaultRouter()

routers.register('company', CompanyViewSet),
routers.register('company_data', CompanyViewSet)


urlpatterns = [

    path('',include(routers.urls))
]