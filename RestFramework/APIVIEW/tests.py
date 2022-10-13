from django.test import TestCase
from .models import Company,Lead
from django.test import Client
from accounts.models import User
from rest_framework.test import APITestCase


class UserLoginTestCase(APITestCase):
  
  def setUp(self):
    pass


  def test_register_user(self):
      response = self.client.post('/apiview/register/', { 'username':'Jeet11','email': 'jm2@gmail.com', 'password': 'Meena@12345'})
      code = response.status_code
      self.assertEqual(code, 200)


  # def test_user_login(self):
  #   c = Client()
  #   response = c.post('/apiview/company_login/', {'email': 'jm1@gmail.com', 'password': 'Meena@12345'})
  #   code = response.status_code
  #   self.assertEqual(code, 200)

class Leads(TestCase):

  @classmethod
  def setUpTestData(cls):
    User.objects.create(username="john",email="tw@gmail.com",password="123")

  def test_email_max_length(self):
    c = Client()
    response = c.get('/apiview/projectlist/')
    author = User.objects.get(id=1)
    max_length = author._meta.get_field('email').max_length
    self.assertEqual(max_length, 255)
    self.assertEqual(response.status_code,200) 



 

