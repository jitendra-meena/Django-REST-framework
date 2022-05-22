
from rest_framework import serializers
from APIVIEW.models import Company, Developer, ProjectManager



class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Company
        fields = '__all__'


