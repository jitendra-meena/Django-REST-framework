from dataclasses import fields
from rest_framework import serializers
from .models import Company,ProjectManager


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = '__all__'
