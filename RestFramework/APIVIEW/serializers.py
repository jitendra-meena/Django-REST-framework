from dataclasses import fields
from rest_framework import serializers
from .models import Company,ProjectManager
from accounts.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CompanyLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=3, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self,obj):
        user = User.objects.get(email = obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user_email = User.objects.filter(email = email)
        user = auth.authenticate(email = email, password = password)

        if user_email.exists() and user_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + user_email[0].auth_provider)
    
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')