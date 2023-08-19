from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from core.models import ActiveUser
from user_management.serializers import UserLoginPhoneSerializer, BaseUserLoginSerializer, UserProfileSerializer
from user_management.helpers import FindUser, UserCreationHelper, LoginCodeCreation, FindUserProfile, send_login_code, InviteCodeHelper


class UserLogin(APIView):
    """User registration"""

    permission_classes = [AllowAny,]

    def post(self, request):
        phone_serializer = UserLoginPhoneSerializer(data=request.data)
        phone_serializer.is_valid(raise_exception=True)

        code = LoginCodeCreation()()
        user = FindUser(phone=phone_serializer.data['phone'])()
    
        if user:
            send_login_code(user=user, code=code)
        else:
            new_user = UserCreationHelper(phone=phone_serializer.data['phone'], login_code=code)()
            send_login_code(user=new_user, code=code)

        return Response(status=status.HTTP_200_OK, data={'code': code})
    

class UserConfirmation(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        user_credentials_serializer = BaseUserLoginSerializer(data=request.data)
        user_credentials_serializer.is_valid(raise_exception=True)

        user = authenticate(request, phone=user_credentials_serializer.data['phone'], password=user_credentials_serializer.data['code'])
        if not user:
            raise APIException('Invalid credentials!')    
        
        login(request, user)
        return Response({'login': True})
    

class UserProfile(APIView):
    def get(self, request):
        user_profile = FindUserProfile(user_id=request.data['user_id'])()
        user_profile_serializer = UserProfileSerializer(user_profile)

        return Response(user_profile_serializer.data)


class ActivateCode(APIView):    
    def post(self, request):
        inv = InviteCodeHelper(user_id=request.data['user_id'], code=request.data['code'])
        to_user_profile = inv.make_decision()
        
        if isinstance(to_user_profile, UserProfile):
            user_profile_serializer = UserProfileSerializer(to_user_profile)
            return Response(user_profile_serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': to_user_profile})


