
from msilib.schema import AppId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company,ProjectManager
from . serializers import ProjectListSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .paginations import CustomPagination
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ProjectList(APIView):
    '''
    Get all Manager List

    Post API For add new manager
    '''
    # permission_classes = (IsAuthenticated,)
    # pagination_class = CustomPagination

    def get(self,request):
        if 'project' in cache:
            project = cache.get('project')
            serializer = ProjectListSerializer(project,many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        else:        
            project = ProjectManager.objects.all()
            serializer = ProjectListSerializer(project,many=True)
            cache.set(project, project, timeout=CACHE_TTL)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
    
    def post(self,request):
        company = request.data.get('company')
        company = Company.objects.get(id = company)
        serializer =  ProjectListSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    


class List(APIView):
    '''
        Get API for particular Manager List

        PUT API for Update Manager Data

        PATCH API for Update particular Field Data

        Delete API for Delete manage by id
    '''
    def get(self,request,manager_id):
        project = ProjectManager.objects.get(id = manager_id)
        serializer = ProjectListSerializer(project)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    
    def put(self,request, manager_id):

        company = request.data.get('company')
        manager = ProjectManager.objects.get(id= manager_id)
        company = Company.objects.get(id = company)
        serializer =  ProjectListSerializer(manager,data =request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request, manager_id):

        company = request.data.get('company')
        manager = ProjectManager.objects.get(id= manager_id)
        company = Company.objects.get(id = company)
        serializer =  ProjectListSerializer(manager,data =request.data,partial=True)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)             

    def delete(self, request, manager_id):
        project = ProjectManager.objects.get(id = manager_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    




# Authentication System


class Register(APIView):
    """
    user Register and get details revert
    """
    
    def get(self,request):
        users = User.objects.all()
        serializers = UserSerializer(users,many=True)
        return Response(status=status.HTTP_200_OK,data=serializers.data)

    def post(self,request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            password = serializers.data.get('password')
            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_200_OK,data=serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class CompanyLogin(APIView):
    """
    Company Login and Validate data
    """

    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CompanyLogout(APIView):
    """
    Company Logout Data 
    """

    def get(self,request):
        logout(request)
        return Response('User Logged out successfully')
   

