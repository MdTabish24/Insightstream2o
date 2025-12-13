import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import HashtagGenerateSerializer
from .services import HashtagService

logger = logging.getLogger(__name__)

class HashtagGenerateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = HashtagGenerateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            service = HashtagService()
            result = service.generate_hashtags(topic=serializer.validated_data['topic'])
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Hashtag generation error: {str(e)}')
            return Response(
                {'error': {'code': 'HASHTAG_GENERATION_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
