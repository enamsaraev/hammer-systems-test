import re

from rest_framework import serializers

from core.models import UserProfile, ActiveUser


class UserLoginPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        if not re.match(r"^[0-9]{11}$", data['phone']):
            raise serializers.ValidationError('Phone should countain only digits')
        
        return data
    

class BaseUserLoginSerializer(serializers.Serializer):
    """User serializer for auth"""
    
    phone = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=255)


class ActiveUserSerializer(serializers.ModelSerializer):
    phone = serializers.StringRelatedField(source='user.phone')

    class Meta:
        model = ActiveUser
        fields = ('phone',)


class UserProfileSerializer(serializers.ModelSerializer):
    active_user_code = serializers.StringRelatedField(source='active_user.invite_code')
    activeusers = ActiveUserSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'activate_code', 'active_user_code', 'activeusers')
    