from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

import os

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class AutoLoginView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username).first()
        
        if not user:
            
            user = User.objects.create_user(username=username, password=password)
            
            authenticate_user = authenticate(username=username, password=password)
            
            if not authenticate_user:
                return Response({'error': 'Authentication failed after user creation.'}, status=status.HTTP_400_BAD_REQUEST)
            
            tokens = get_tokens_for_user(authenticate_user)
            response = Response(tokens, status=status.HTTP_200_OK)
            
            isProduction = os.getenv('DJANGO_ENV') == 'production'

            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=isProduction,
                samesite='None' if isProduction else 'Lax',
            )

            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=isProduction,
                samesite='None' if isProduction else 'Lax',
            )
            return response
