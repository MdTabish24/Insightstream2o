from rest_framework import serializers

class OutlierSerializer(serializers.Serializer):
    channel_id = serializers.CharField(max_length=100)

class UploadStreakSerializer(serializers.Serializer):
    channel_id = serializers.CharField(max_length=100)

class ThumbnailSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200, required=False)
    image_url = serializers.URLField(required=False)
