from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework.decorators import api_view
from rest_framework import status
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import check_password
import secrets
from django.core.mail import send_mail
from django.http import HttpResponse
from .utils import generate_verification_token
from django.template.loader import render_to_string



# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate verification token
        token = generate_verification_token()
        user.verification_token = token
        user.save()

        # Send verification email
        send_verification_email(user)

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
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        print(token)
        user_id=jwt.decode(token,'secret', algorithms=['HS256'])['id']
        print(User.objects.get(id=user_id))

        # Set JWT token as a cookie in the response
        response = Response()
        self.set_cookie(response, key='jwt', value=token) 

        # Return JWT token in response data
        response.data = {
            "message":"success",
            "token": token,  # Decode here if needed
            "user": UserSerializer(user).data
        }
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
        response.delete_cookie('token')
        response.delete_cookie('user')
        response.data = {
            'message': 'Logout success.'
        }
        return response

class allUsers(APIView):
    def get(self,request):
        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'model':'User', 'Users':dataJSON}) 
    

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
def delete(request, id):
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

    # Get the password from the request
    password = request.data.get('password', '')

    # Check if the password is provided
    if not password:
        return Response({'msg': 'Please provide your password to delete your account'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the user
    user = User.objects.filter(id=id).first()

    # Check if user exists
    if not user:
        return Response({'msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Verify the password
    if not check_password(password, user.password):
        return Response({'msg': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete the user
    user.delete()
    return Response({'msg': 'User Deleted'})



def verify_email(request):
    token = request.GET.get('token')
    if token:
        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True
            user.save()
            return HttpResponse('Email verified successfully!')
        except User.DoesNotExist:
            return HttpResponse('Invalid token!')
    else:
        return HttpResponse('Token parameter is missing!')
    

def send_verification_email(user):
    subject = 'Email Verification'
    message = f'Click the following link to verify your email: http://localhost:8000/verify-email?token={user.verification_token}'
    send_mail(subject, message, 'taghreedmuhammed7@gmail.com', [user.email])
