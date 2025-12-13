from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AIContent
from .serializers import AIContentSerializer, ContentGenerateSerializer
from .services import content_service
from core.exceptions import AIServiceUnavailable, InsightStreamException

class ContentGenerateView(generics.CreateAPIView):
    """
    Generate AI video content concepts.
    
    POST /api/content/generate/
    Body: {"topic": "your topic"}
    
    Requirements:
    - 3.1: Return 3 unique video concepts
    - 3.2: Include SEO scores (0-100)
    - 3.3: Include hooks, main content, CTAs
    - 3.4: Fallback on AI failure
    - 3.5: Store in database
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ContentGenerateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            result = content_service.generate_content(
                topic=serializer.validated_data['topic'],
                user=request.user
            )
            return Response(result, status=status.HTTP_201_CREATED)
            
        except AIServiceUnavailable as e:
            return Response({
                'error': {
                    'code': 'AI_SERVICE_UNAVAILABLE',
                    'message': str(e.message),
                    'details': {}
                }
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except InsightStreamException as e:
            return Response({
                'error': {
                    'code': e.code,
                    'message': e.message,
                    'details': {}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'Failed to generate content',
                    'details': {'error': str(e)}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentHistoryView(generics.ListAPIView):
    """
    Get user's content generation history.
    
    GET /api/content/history/
    
    Requirements:
    - 11.2: Return all content for user
    - 11.3: Ordered by creation date descending
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AIContentSerializer
    
    def get_queryset(self):
        return AIContent.objects.filter(user=self.request.user)
