from dataclasses import fields
from rest_framework import serializers
from .models import Company,ProjectManager
from django.contrib.auth.models import User


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
