import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company,ProjectManager, Developers,Developer,Lead
from . serializers import ( 
    ProjectListSerializer,
    UserSerializer,
    CompanyLoginSerializer,
    LogoutSerializer,
    EmailVerificationSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    DevelopersSerializer
    )
from rest_framework.permissions import IsAuthenticated
from .paginations import CustomPagination
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from accounts.models import User
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
import jwt
from django.shortcuts import redirect

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ProjectList(APIView):
    '''
    Get all Manager List

    Post API For add new manager
    '''
    # permission_classes = (IsAuthenticated,)
    # pagination_class = CustomPagination

    def get(self,request):
        if 'project' in cache:
            project = cache.get('project')
            serializer = ProjectListSerializer(project,many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        else:        
            project = ProjectManager.objects.all()
            serializer = ProjectListSerializer(project,many=True)
            cache.set(project, project, timeout=CACHE_TTL)
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




# Authentication System


class Register(APIView):
    """
    user Register and get details revert
    """
    
    def get(self,request):
        users = User.objects.all()
        serializers = UserSerializer(users,many=True)
        return Response(status=status.HTTP_200_OK,data=serializers.data)

    def post(self,request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            password = serializers.data.get('password')
            user.set_password(password)
            user.save()
            user_data = serializers.data
            user = User.objects.get(email=user_data['email'])
            token =RefreshToken.for_user(user).access_token
            breakpoint()
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.username + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)
            return Response(status=status.HTTP_200_OK,data=serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class CompanyLogin(APIView):
    
    """
    Company Login and Validate data
    """
    serializer_class = CompanyLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyLogout(APIView):
    serializer_class = LogoutSerializer

    """
    Company Logout Data 
    """

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
   

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmail(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(APIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class Developers(APIView):
    # queryset = Developers.objects.all()
    serializer_class = DevelopersSerializer

    def get(self,request, *args, **kwargs):
        developer = Developer.objects.all()
        serializer = DevelopersSerializer(developer,many = True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer = DevelopersSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        lead = Lead.objects.get(id = request.data.get('lead'))
        project_manager = ProjectManager.objects.get(id = request.data.get('project_manager'))
        serializer.save(lead=lead,project_manager =project_manager)
        return Response(data = serializer.data,status = status.HTTP_200_OK)


    