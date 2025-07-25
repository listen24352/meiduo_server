from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import logout


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response({'code': 0, 'errmsg': 'ok'}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('username')
        return response
