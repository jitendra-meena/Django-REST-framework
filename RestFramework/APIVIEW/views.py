
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company,ProjectManager
from . serializers import ProjectListSerializer
from rest_framework.permissions import IsAuthenticated
from .paginations import CustomPagination
from django.core.paginator import Paginator


class ProjectList(APIView):
    '''
    Get all Manager List

    Post API For add new manager
    '''
    # permission_classes = (IsAuthenticated,)
    # pagination_class = CustomPagination

    def get(self,request):
        project = ProjectManager.objects.all()
        page_number = self.request.query_params.get('page_number ', 1)
        page_size = self.request.query_params.get('page_size ', 3)

        paginator = Paginator(project , page_size)
        serializer = ProjectListSerializer(paginator.page(page_number),many=True)
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
