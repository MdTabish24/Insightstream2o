from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import KeywordResearchSerializer
from .services import keyword_service
from core.exceptions import AIServiceUnavailable, YouTubeAPIError, InsightStreamException

class KeywordResearchView(APIView):
    """
    Keyword research endpoint.
    
    POST /api/keywords/research/
    Body: {"topic": "your topic"}
    
    Requirements:
    - 4.1: Return primary keywords with search volume
    - 4.2: Return long-tail keywords
    - 4.3: Return trending keywords from YouTube
    - 4.4: Return related topics
    - 4.5: Include metadata (search volume, competition, relevance)
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = KeywordResearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            result = keyword_service.research_keywords(
                topic=serializer.validated_data['topic']
            )
            return Response(result, status=status.HTTP_200_OK)
            
        except AIServiceUnavailable as e:
            return Response({
                'error': {
                    'code': 'AI_SERVICE_UNAVAILABLE',
                    'message': str(e.message),
                    'details': {}
                }
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except YouTubeAPIError as e:
            return Response({
                'error': {
                    'code': 'YOUTUBE_API_ERROR',
                    'message': str(e.message),
                    'details': {}
                }
            }, status=status.HTTP_502_BAD_GATEWAY)
            
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
                    'message': 'Failed to research keywords',
                    'details': {'error': str(e)}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
