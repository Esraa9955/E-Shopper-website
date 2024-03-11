from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from rest_framework import status
import datetime
from rest_framework import status
from django.core.mail import send_mail
from django.http import HttpResponse
from .utils import generate_verification_token
from .models import CustomToken
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import check_password
from .models import PasswordResetOTP
import random
from django.utils import timezone
from django.conf import settings

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
        user = User.objects.get(id=request.user.id)

        # Check if the user's token has expired
        token = CustomToken.objects.get(user=user)
        if token.expires and token.is_expired():
            raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})

        # Check if the provided password is correct
        password = request.data.get('password', None)
        if not password or not check_password(password, user.password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        user_delete = User.objects.filter(id=request.user.id).delete()
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

def send_reset_password_otp(email, otp):
    subject = 'Reset Your Password'
    message = f'Your OTP for password reset is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate 6-digit OTP
        expires_at = timezone.now() + timezone.timedelta(minutes=15)  # OTP expires in 15 minutes

        # Save OTP in the database
        PasswordResetOTP.objects.update_or_create(email=email, defaults={'otp': otp, 'expires_at': expires_at})

        # Send OTP to the user's email
        send_reset_password_otp(email, otp)

        return Response({'message': 'OTP sent to your email. Check your inbox.'})

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_obj = PasswordResetOTP.objects.get(email=email, otp=otp)
            if not otp_obj.is_expired():
                # Reset user's password
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                otp_obj.delete()
                return Response({'message': 'Password reset successfully.'})
            else:
                return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetOTP.DoesNotExist:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
