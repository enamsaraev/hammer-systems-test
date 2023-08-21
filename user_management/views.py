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
    """
        User login/registration
        POST: phone
    """

    permission_classes = [AllowAny,]

    def post(self, request):
        phone_serializer = UserLoginPhoneSerializer(data=request.data)
        phone_serializer.is_valid(raise_exception=True)

        code = LoginCodeCreation()()
        user = FindUser(phone=phone_serializer.data['phone'])()
    
        if user:
            send_login_code(user=user, code=code)
            return Response(status=status.HTTP_200_OK, data={'code': code})
        elif not user:
            new_user = UserCreationHelper(phone=phone_serializer.data['phone'], login_code=code)()
            send_login_code(user=new_user, code=code)
            return Response(status=status.HTTP_201_CREATED, data={'code': code})
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserConfirmation(APIView):
    """
        Confirmation view (get code by phone number)
        POST: phone, code
    """
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
    """
        Return user profile
        GET: user_id
    """
    def get(self, request):
        user_profile = FindUserProfile(user_id=request.data['user_id'])()
        user_profile_serializer = UserProfileSerializer(user_profile)

        return Response(user_profile_serializer.data)


class ActivateCode(APIView):    
    """
        Invite code enter
        POST: user_id (who activate code), code (whos code is activated)
    """
    def post(self, request):
        inv = InviteCodeHelper(user_id=request.data['user_id'], code=request.data['code'])
        to_user_profile = inv.make_decision()

        if not isinstance(to_user_profile, str):
            user_profile_serializer = UserProfileSerializer(to_user_profile)
            return Response(status=status.HTTP_200_OK, data={'activated_profile': user_profile_serializer.data})
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


