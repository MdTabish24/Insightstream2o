from rest_framework import serializers
from .models import Thumbnail

class ThumbnailSerializer(serializers.ModelSerializer):
    """Serializer for thumbnail model"""
    class Meta:
        model = Thumbnail
        fields = ['id', 'user_input', 'thumbnail_url', 'ref_image', 'created_at']
        read_only_fields = ['id', 'thumbnail_url', 'created_at']

class ThumbnailGenerateSerializer(serializers.Serializer):
    """Serializer for thumbnail generation request"""
    prompt = serializers.CharField(
        max_length=500,
        min_length=3,
        help_text='Description of the thumbnail to generate (3-500 characters)',
        error_messages={
            'min_length': 'Prompt must be at least 3 characters long',
            'max_length': 'Prompt must not exceed 500 characters'
        }
    )
    ref_image = serializers.URLField(
        required=False,
        allow_blank=True,
        help_text='Optional reference image URL for style matching'
    )
    
    def validate_prompt(self, value):
        """Validate prompt is not just whitespace"""
        if not value.strip():
            raise serializers.ValidationError('Prompt cannot be empty or just whitespace')
        return value.strip()
