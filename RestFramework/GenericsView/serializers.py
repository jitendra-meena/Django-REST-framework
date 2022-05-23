
from rest_framework import serializers
from APIVIEW.models import Company, Developer, ProjectManager



class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Developer
        fields = '__all__'


class UpdateManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model =  ProjectManager
        fields = '__all__'

