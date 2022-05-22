from functools import partial
import imp
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company,ProjectManager
from . serializers import ProjectListSerializer



class ProjectList(APIView):

    def get(self,request):
        project = ProjectManager.objects.all()
        serializer = ProjectListSerializer(project,many=True)
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
