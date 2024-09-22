from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('uuid', 'email', 'full_name', 'password','created_at', 'updated_at')  # Add/modify fields as needed
    
    def create(self, validated_data):
        try:
            # Set full_name as the username
            username = validated_data['full_name']
            
            # Create user with full_name as username, and other required fields
            user = CustomUser(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                username=username,  # Set full_name as the username
            )
            user.set_password(validated_data['password'])
            user.save()
            return user  # Ensure the created user is returned
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError("An error occurred while creating the user.")  # Return a validation error

    def validate_email(self, value):
        # Custom validation to ensure email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
