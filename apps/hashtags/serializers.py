from rest_framework import serializers

class HashtagGenerateSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200, required=True)
    
    def validate_topic(self, value):
        if not value.strip():
            raise serializers.ValidationError('Topic cannot be empty')
        return value.strip()
