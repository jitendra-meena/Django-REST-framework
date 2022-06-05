from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):           # ↓ Here ↓
    id = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    last_login = models.CharField(max_length=100)
    is_superuser = models.CharField(max_length=100) # ↓ Here
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone = models.IntegerField()
    is_staff = models.CharField(max_length=100)
    is_active = models.CharField(max_length=100)
    date_joined = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    

    objects = CustomUserManager()
    


    USERNAME_FIELD: 'email'
    REQUIRED_FIELDS = []