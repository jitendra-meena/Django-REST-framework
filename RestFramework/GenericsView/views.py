
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView , RetrieveUpdateDestroyAPIView
from APIVIEW.models import Company, Developer, ProjectManager
from . serializers import DeveloperSerializer, UpdateManagerSerializer


class Developer(ListCreateAPIView):
    
    """
    Get and Post API Developer data add and get.

    we can custimize Response according Requirements.

    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class UpdateManager(RetrieveUpdateDestroyAPIView):
    
    """
    Get and Post,PUT and delete API for perfom action on Developer data .

    we can custimize Response according Requirements.

    """
    queryset = ProjectManager.objects.all()
    serializer_class = UpdateManagerSerializer

