from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Thumbnail
from .serializers import ThumbnailSerializer, ThumbnailGenerateSerializer
from .services import thumbnail_service
from core.exceptions import AIServiceUnavailable, InsightStreamException

class ThumbnailGenerateView(generics.CreateAPIView):
    """
    Generate AI thumbnail endpoint.
    
    POST /api/thumbnails/generate/
    Body: {"prompt": "your prompt", "ref_image": "optional_url"}
    
    Requirements:
    - 2.1: Generate using FLUX AI model
    - 2.2: Fallback to Pollinations if FLUX fails
    - 2.3: Upload to ImageKit and store in database
    - 2.6: 16:9 aspect ratio, PNG format
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ThumbnailGenerateSerializer
    
    def create(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"[ThumbnailView] Received request from user: {request.user.email}")
        logger.info(f"[ThumbnailView] Request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.info(f"[ThumbnailView] Validation passed. Prompt: {serializer.validated_data['prompt'][:50]}...")
        
        try:
            logger.info(f"[ThumbnailView] Calling thumbnail_service.generate_thumbnail...")
            result = thumbnail_service.generate_thumbnail(
                prompt=serializer.validated_data['prompt'],
                ref_image=serializer.validated_data.get('ref_image'),
                user=request.user
            )
            logger.info(f"[ThumbnailView] Success! Thumbnail ID: {result.get('id')}, URL: {result.get('thumbnail_url')[:100]}...")
            return Response(result, status=status.HTTP_201_CREATED)
            
        except AIServiceUnavailable as e:
            logger.error(f"[ThumbnailView] AI Service Unavailable: {str(e.message)}")
            return Response({
                'error': {
                    'code': 'AI_SERVICE_UNAVAILABLE',
                    'message': str(e.message),
                    'details': {}
                }
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except InsightStreamException as e:
            logger.error(f"[ThumbnailView] InsightStream Exception: {e.code} - {e.message}")
            return Response({
                'error': {
                    'code': e.code,
                    'message': e.message,
                    'details': {}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            logger.error(f"[ThumbnailView] Unexpected error: {str(e)}", exc_info=True)
            return Response({
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'Failed to generate thumbnail',
                    'details': {'error': str(e)}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ThumbnailHistoryView(generics.ListAPIView):
    """
    Get user's thumbnail history.
    
    GET /api/thumbnails/history/
    
    Requirements:
    - 2.5: Return all thumbnails for user
    - 11.3: Ordered by creation date descending
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ThumbnailSerializer
    
    def get_queryset(self):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[ThumbnailHistory] Fetching history for user: {self.request.user.email}")
        queryset = Thumbnail.objects.filter(user=self.request.user)
        logger.info(f"[ThumbnailHistory] Found {queryset.count()} thumbnails")
        return queryset
