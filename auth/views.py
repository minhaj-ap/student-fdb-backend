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
      
class CustomLoginView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username).first()
        
        if not user:
            
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        authenticate_user = authenticate(username=username, password=password)
            
        if not authenticate_user:
            return Response({'error': 'Authentication failed.'}, status=status.HTTP_400_BAD_REQUEST)
            
        tokens = get_tokens_for_user(authenticate_user)
        user_data = {
            'id': authenticate_user.id,
            'username': authenticate_user.username,
            'is_staff': authenticate_user.is_staff,
            'is_superuser': authenticate_user.is_superuser,
            'is_active': authenticate_user.is_active,
        }
        response = Response({'tokens': tokens, 'user': user_data}, status=status.HTTP_200_OK)

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
    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        tokens = get_tokens_for_user(user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        }
        
        response= Response({'tokens': tokens, 'user': user_data}, status=status.HTTP_201_CREATED)
        
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
    
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            response = Response({'access': new_access_token}, status=status.HTTP_200_OK)

            isProduction = os.getenv('DJANGO_ENV') == 'production'

            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=isProduction,
                samesite='None' if isProduction else 'Lax',
            )

            return response
        except Exception as e:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        

