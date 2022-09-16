from django.urls import path,include
from rest_framework import routers
from .views import CompanyViewSet, CompanyVDataiewSet, CompanyModelViewSet

routers = routers.DefaultRouter()

routers.register('company', CompanyViewSet),
routers.register('company_data', CompanyViewSet)
routers.register('CompanyModelViewSet',CompanyModelViewSet)


urlpatterns = [

    path('',include(routers.urls))
]