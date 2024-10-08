from rest_framework import serializers,fields
from djoser.serializers import UserCreateSerializer,PasswordResetConfirmSerializer
from djoser.utils import decode_uid
from users.models import CustomUser
from django.contrib.auth import get_user_model
# import settings
from django.conf import settings
import logging
import requests
User=get_user_model()
logger = logging.getLogger(__name__)

class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True, required=False)  

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('uuid', 'email', 'full_name', 'password', 'created_at', 'updated_at')  

    def create(self, validated_data):
        try:
            # Set full_name as the username
            # Create user with full_name as username, and other required fields
            user = CustomUser(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user  # Ensure the created user is returned
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError("An error occurred while creating the user.")
    def update(self, instance, validated_data):
        # Placeholder for update logic
        return super().update(instance, validated_data)
    def validate_email(self, value):
        # Custom validation to ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

# users/serializers.py
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('uuid', 'email', 'full_name', 'created_at', 'updated_at')
        read_only_fields = ('uuid', 'created_at', 'updated_at')

class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Check if both passwords match
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({"new_password": [_("Passwords must match.")]})
        return attrs
    
    # save the new password
    def save(self):
        # Decode the UID and retrieve the user
        try:
            uid = decode_uid(self.validated_data['uid'])
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"uid": _("Invalid UID or User not found.")})
        
        # Set the new password and save the user
        user.set_password(self.validated_data['new_password'])
        user.save()

class GoogleSocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    code=serializers.CharField(required=True)
    id_token = serializers.CharField(required=True)
    class Meta:
        fields = ['access_token', 'code', 'id_token']

    def validate_access_token(self, value):
        # Validate the access token by sending a request to Google
        google_token_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        response = requests.get(f'{google_token_info_url}?access_token={value}')
        
        if response.status_code != 200:
            raise serializers.ValidationError("Invalid access token")

        token_info = response.json()

        # Validate that the token audience matches the app's Google client ID
        if token_info.get('aud') != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
            raise serializers.ValidationError("Invalid token audience")
        
        return value