from rest_framework import serializers

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    
    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError('Username cannot be empty')
        return value.strip()
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('Password cannot be empty')
        return value
