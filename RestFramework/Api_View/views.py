
from functools import partial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from APIVIEW.models import Company, Developer, ProjectManager
from .serializers import DeveloperSerializer

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def developers(self,request):

    """
        CRUD Operation using api_view
        perform all opertion on Developer Data
    """
    if request.method == 'GET':
        id = request.data.get('id')
        if id is not None:
            dev = Developer.objects.get(id=id)
            serializer = DeveloperSerializer(dev)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        dev = Developer.objects.all()
        serializer = DeveloperSerializer(dev,many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)

    if request.method == 'POST':

        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        return Response(serializer.errors)

    if request.method == 'PUT':
        id = request.data.get('id')
        developer = Developer.objects.get(id =id)
        serializer = DeveloperSerializer(developer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        return Response(serializer.errors)  


    if request.method == 'PATCH':
        id = request.data.get('id')
        developer = Developer.objects.get(id =id)
        serializer = DeveloperSerializer(developer,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        return Response(serializer.errors)                  

    if request.method == 'DELETE':
        id = request.data.get(id)
        developer = Developer.objects.get(id =id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
