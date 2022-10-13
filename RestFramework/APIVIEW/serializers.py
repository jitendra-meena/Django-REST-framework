from rest_framework import serializers
from .models import Company,ProjectManager,Developer,Lead
from accounts.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = '__all__'
        




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

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


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)    


class LeadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id']


class DevelopersSerializer(serializers.ModelSerializer):
    # exaperience_total = serializers.SerializerMethodField()
    # lead = LeadSerializers()

    class Meta:
        model = Developer
        fields = "__all__"
        depth = 1

    # def get_exaperience_total(self,obj):
        # return obj.experience    

class DevelopersPOSTSerializer(serializers.ModelSerializer):
    # exaperience_total = serializers.SerializerMethodField()
    lead = serializers.SlugRelatedField(slug_field="id", read_only=False, queryset=Lead.objects.all())
    project_manager = serializers.SlugRelatedField(slug_field="id", read_only=False, queryset=ProjectManager.objects.all())

    class Meta:
        model = Developer
        fields = "__all__"
        depth = 1 
