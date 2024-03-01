from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework import permissions
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status



# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def set_cookie(self, response, key, value, expire=None):
        if expire is None:
            max_age = 3600  
        else:
            max_age = expire
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires, secure=settings.SESSION_COOKIE_SECURE or None)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return Response({'message': 'Email and password are required!'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # expiration 1h
            'iat': datetime.datetime.utcnow() # tokenCreatedAt
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Set JWT token as a cookie in the response
        response = Response()
        self.set_cookie(response, key='jwt', value=token) 

        # Return JWT token in response data
        response.data = {'jwt': token}
        
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success.'
        }
        return response

class allUsers(APIView):
    def get(self,request):
        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'model':'User', 'Users':dataJSON}) 
    

    
# class IsAuthenticatedUser(BasePermission):
#     def has_permission(self, request, view, id):
#         is_authenticated = request.user.is_authenticated and request.user.id == id
#         return is_authenticated

        
    

@api_view(['PUT'])
def UpdateUserView(request, id):
    token = request.COOKIES.get('jwt')

    # Check if user is authenticated
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    # Check if the authenticated user is the same as the user being updated
    if payload['id'] != id:
        return Response({'msg': 'You are not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)

    update_object = User.objects.filter(id=id).first()
    if update_object:
        serialized_user = UserSerializer(instance=update_object, data=request.data, partial=True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(data=serialized_user.data)
        else:
            print(serialized_user.errors)  # Print serializer errors for debugging
            return Response({'msg': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete(request,id):
    token = request.COOKIES.get('jwt')

    # Check if user is authenticated
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    # Check if the authenticated user is the same as the user being deleted
    if payload['id'] != id:
        return Response({'msg': 'You are not authorized to delete this user'}, status=status.HTTP_403_FORBIDDEN)

    us=User.objects.filter(id=id).first()
    if(us):
        User.objects.filter(id=id).delete()
        return Response({'msg':'User Deleted'}) 
    return Response({'msg':'User Not Found'})





