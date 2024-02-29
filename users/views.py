from django.shortcuts import render
from rest_framework.exceptions import NotFound
from django.shortcuts import render
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


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # expiration 1h
            'iat': datetime.datetime.utcnow() # tokenCreatedAt
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token  # Decode here if needed
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
        response.data = {
            'message': 'Logout success.'
        }
        return response

class allUsers(APIView):
    def get(self,request):
        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'model':'User', 'Users':dataJSON}) 
    

    
class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated, IsAuthenticatedUser])
def UpdateUserView(request, id):
    update_object = User.objects.filter(id=id).first()
    if update_object:
        serialized_user = UserSerializer(instance=update_object, data=request.data, partial=True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(data=serialized_user.data)
        else:
            print(serialized_user.errors)  # Print serializer errors for debugging
            return Response({'msg':'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg':'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsAuthenticatedUser])
def delete(request,id):
  us=User.objects.filter(id=id).first()
  if(us):
     User.objects.filter(id=id).delete()
     return Response({'msg':'User Deleted'}) 
  return Response({'msg':'User Not Found'})





