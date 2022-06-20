import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ActiveUserMiddleware(MiddlewareMixin):
    def _init_(self, get_response):
      self.get_response = get_response

    def _call_(self, request):

        

        response = self.get_response(request)
        response.write("<p></p><hr/><div style='color:blue;text-align:center'>Copyright © Srikanth Technologies. All rights reserved.</div>")
        print(list(response))
        print(type(response),"Res")
        # Code that is executed in each request after the view is called
        return response 

    # def middleware(self,request):
    #   response = self.get_response(request)
    #   response.write("<p></p><hr/><div style='color:blue;text-align:center'>Copyright © Srikanth Technologies. All rights reserved.</div>")
    #   print(list(response))
    #   print(type(response),"Res")
    #   print(response,"Res")
    #   # Code that is executed in each request after the view is called
    #   return response 


    def process_request(self, request):
        print(self.get_response,"Response")
        current_user = request.user
        print(current_user,"Current User")
        response = self.get_response(request)
        # response.data['detail'] = 'bla-bla-bla'
        print(type(response),"Data")
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set('seen_%s' % (current_user.username), now, 
                           settings.USER_LASTSEEN_TIMEOUT)

    def process_template_response(self, request, response):
      if hasattr(response, 'data'): 
          response.data['detail'] = 'bla-bla-bla'
          print(response.data,"Data")
      return response                       