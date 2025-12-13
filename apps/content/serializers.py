from rest_framework import serializers
from .models import AIContent

class AIContentSerializer(serializers.ModelSerializer):
    """Serializer for AI content model"""
    class Meta:
        model = AIContent
        fields = ['id', 'user_input', 'content', 'thumbnail_url', 'created_at']
        read_only_fields = ['id', 'content', 'created_at']

class ContentGenerateSerializer(serializers.Serializer):
    """Serializer for content generation request"""
    topic = serializers.CharField(
        max_length=500,
        min_length=3,
        help_text='Topic for video content generation (3-500 characters)',
        error_messages={
            'min_length': 'Topic must be at least 3 characters long',
            'max_length': 'Topic must not exceed 500 characters'
        }
    )
    
    def validate_topic(self, value):
        """Validate topic is not just whitespace"""
        if not value.strip():
            raise serializers.ValidationError('Topic cannot be empty or just whitespace')
        return value.strip()
