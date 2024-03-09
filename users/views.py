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
from .models import CustomToken
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'message': 'This Email Is already Exists!'}, status=status.HTTP_400_BAD_REQUEST)

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
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        if not user.is_active:
            raise AuthenticationFailed('Please Active Email First!')

        response = Response()

        token, created = CustomToken.objects.get_or_create(user=user)
        token.save()

        response.data = {
            "message":"success",
            "token": token.key,
            "user": UserSerializer(user).data,
        }
        return response
        



class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get user
    def get(self, request):
        try:
            user = User.objects.get(id = request.user.id)
                        
            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
            return Response({'message': UserSerializer(user).data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try:
            user = User.objects.get(id = request.user.id)

            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
            user = User.userDelete(request.user.id)
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request):
        try:
            id = request.user.id
            user = User.objects.get(id=id)

            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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
        
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            token = CustomToken.objects.get(user=request.user.id)
            token.delete()
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({"message":'user is already logged out.'})

        response = Response({'message': 'Logout success.'}, status=status.HTTP_200_OK)
        return response

class allUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser & IsAuthenticated]

    def get(self,request):
        # Check if the user's token has expired
        try:
            user = get_object_or_404(User, id=request.user.id)
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({"data": "missing_token", "message": 'Token not found for the user.'})

        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'Users':dataJSON})


# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.delete_cookie('token')
#         response.delete_cookie('user')
#         response.data = {
#             'message': 'Logout success.'
#         }
#         return response

# class allUsers(APIView):
#     def get(self,request):
#         users=User.usersList()
#         dataJSON=UserSerializer(users,many=True).data
#         return Response({'model':'User', 'Users':dataJSON}) 
    

# @api_view(['PUT'])
# def UpdateUserView(request, id):
#     token = request.COOKIES.get('jwt')

#     # Check if user is authenticated
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')

#     try:
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated!')

#     # Check if the authenticated user is the same as the user being updated
#     if payload['id'] != id:
#         return Response({'msg': 'You are not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)

#     update_object = User.objects.filter(id=id).first()
#     if update_object:
#         serialized_user = UserSerializer(instance=update_object, data=request.data, partial=True)
#         if serialized_user.is_valid():
#             serialized_user.save()
#             return Response(data=serialized_user.data)
#         else:
#             print(serialized_user.errors)  # Print serializer errors for debugging
#             return Response({'msg': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['DELETE'])
# def delete(request, id):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated!')
#     if payload['id'] != id:
#         return Response({'msg': 'You are not authorized to delete this user'}, status=status.HTTP_403_FORBIDDEN)
#     password = request.data.get('password', '')
#     if not password:
#         return Response({'msg': 'Please provide your password to delete your account'}, status=status.HTTP_400_BAD_REQUEST)
#     user = User.objects.filter(id=id).first()
#     if not user:
#         return Response({'msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
#     if not check_password(password, user.password):
#         return Response({'msg': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
#     user.delete()
#     return Response({'msg': 'User Deleted'})



def verify_email(request):
    token = request.GET.get('token')
    if token:
        try:
            user = User.objects.get(verification_token=token)
            user.is_active = True
            user.save()
            return HttpResponse('<h1>Email verified successfully!</h1> <a href="http://localhost:3000/login" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">Go To Login Page</a>')
        except User.DoesNotExist:
            return HttpResponse('Invalid token!')
    else:
        return HttpResponse('Token parameter is missing!')
    

def send_verification_email(user):
    subject = 'Email Verification'
    message = f'Click the following link to verify your email: http://localhost:8000/verify-email?token={user.verification_token}'
    send_mail(subject, message, 'taghreedmuhammed7@gmail.com', [user.email])
