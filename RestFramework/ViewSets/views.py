from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from APIVIEW.models import Company
from .serializers import CompanySerializer
from rest_framework.viewsets import GenericViewSet

class CompanyViewSet(ViewSet):
    queryset = Company.objects.all()


    def list(self, request):
        serilizer = CompanySerializer(self.queryset, many = True) 
        return Response(serilizer.data)

    
    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = CompanySerializer(item)
        return Response(serializer.data)    


# Generic ViewSet in Djangi Rest Famework...

class CompanyVDataiewSet(GenericViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)