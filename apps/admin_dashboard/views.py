import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import AdminLoginSerializer
from .services import AdminService

logger = logging.getLogger(__name__)

class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = AdminLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            service = AdminService()
            if service.authenticate(
                serializer.validated_data['username'],
                serializer.validated_data['password']
            ):
                request.session['is_admin'] = True
                logger.info('Admin login successful')
                return Response(
                    {'message': 'Login successful', 'authenticated': True},
                    status=status.HTTP_200_OK
                )
            
            logger.warning('Failed admin login attempt')
            return Response(
                {'error': {'code': 'UNAUTHORIZED', 'message': 'Invalid credentials'}},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(f'Admin login error: {str(e)}')
            return Response(
                {'error': {'code': 'INTERNAL_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminStatsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            if not request.session.get('is_admin'):
                return Response(
                    {'error': {'code': 'FORBIDDEN', 'message': 'Admin access required'}},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            service = AdminService()
            stats = service.get_stats()
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Admin stats error: {str(e)}')
            return Response(
                {'error': {'code': 'INTERNAL_ERROR', 'message': str(e)}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
