from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'created_at']
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        style={'input_type': 'password'},
        help_text='Password must be at least 8 characters long'
    )
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()
    
    def validate_password(self, value):
        """Validate password strength using Django's validators"""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        return User.objects.create_user(**validated_data)
