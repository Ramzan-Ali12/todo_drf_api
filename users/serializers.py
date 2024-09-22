from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field='username'

    def validate(self, attrs):
        # Extract the username and password fields
        """
        Validate the given username and password.

        If the credentials are invalid, raise a
        `serializers.ValidationError` with a message indicating that the
        credentials are invalid.

        If the credentials are valid, return the validated data, which
        should be a dictionary containing the username and password.

        :param attrs: The attributes to validate. This is a dictionary
            containing the username and password.
        :type attrs: dict
        :return: The validated data.
        :rtype: dict
        :raises serializers.ValidationError: If the credentials are invalid.
        """
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        if username and password:
            # Authenticate using username
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('No active account found with the given credentials')

            # If authenticated, proceed with token generation
            data = super().validate(attrs)
            return data
        else:
            raise serializers.ValidationError('Both username and password are required.')


class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('uuid', 'email', 'full_name', 'password')

    def validate_email(self, value):
        """
        Custom validation to ensure email is unique.
        If an email already exists in the database, raise a validation error with a custom message.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Please use a different email.")
        return value

    def create(self, validated_data):
        # Handle any potential validation issues during creation without overriding validation messages
        try:
            # Use the manager to create a user, ensuring proper handling of the unique email
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                password=validated_data['password']
            )
            return user
        except serializers.ValidationError as e:
            # If a validation error occurs, log it and re-raise the same error (without overriding)
            logger.error(f"Validation error creating user: {e}")
            raise e
        except Exception as e:
            # Log and raise generic errors (non-validation related) 
            logger.error(f"Error creating user with email {validated_data.get('email')}: {e}")
            raise serializers.ValidationError("There was an error creating the user, please try again.")
