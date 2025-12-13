from rest_framework import serializers

class KeywordResearchSerializer(serializers.Serializer):
    """Serializer for keyword research request"""
    topic = serializers.CharField(
        max_length=200,
        min_length=2,
        help_text='Topic for keyword research (2-200 characters)',
        error_messages={
            'min_length': 'Topic must be at least 2 characters long',
            'max_length': 'Topic must not exceed 200 characters'
        }
    )
    
    def validate_topic(self, value):
        """Validate topic is not just whitespace"""
        if not value.strip():
            raise serializers.ValidationError('Topic cannot be empty or just whitespace')
        return value.strip()
