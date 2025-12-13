import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OutlierSerializer, UploadStreakSerializer, ThumbnailSearchSerializer
from .services import AnalyticsService

logger = logging.getLogger(__name__)

class OutlierView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            channel_id = request.query_params.get('channel_id')
            if not channel_id:
                return Response(
                    {'error': {'code': 'VALIDATION_ERROR', 'message': 'channel_id required'}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            service = AnalyticsService()
            result = service.detect_outliers(channel_id=channel_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Outlier detection error: {str(e)}')
            return Response(
                {'error': {'code': 'OUTLIER_DETECTION_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UploadStreakView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            channel_id = request.query_params.get('channel_id')
            if not channel_id:
                return Response(
                    {'error': {'code': 'VALIDATION_ERROR', 'message': 'channel_id required'}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            service = AnalyticsService()
            result = service.analyze_upload_streak(channel_id=channel_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Upload streak analysis error: {str(e)}')
            return Response(
                {'error': {'code': 'UPLOAD_STREAK_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ThumbnailSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            query = request.query_params.get('query')
            image_url = request.query_params.get('image_url')
            
            if not query and not image_url:
                return Response(
                    {'error': {'code': 'VALIDATION_ERROR', 'message': 'query or image_url required'}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = AnalyticsService()
            result = service.search_thumbnails(query=query, image_url=image_url)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Thumbnail search error: {str(e)}')
            return Response(
                {'error': {'code': 'THUMBNAIL_SEARCH_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
