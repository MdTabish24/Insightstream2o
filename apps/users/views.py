from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db import IntegrityError
from .serializers import UserSerializer, RegisterSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    Validates email uniqueness and password strength.
    Returns user data and JWT tokens on success.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            return Response({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email already exists',
                    'details': {'email': ['A user with this email already exists.']}
                }
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveAPIView):
    """
    Get authenticated user profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    """
    Logout endpoint - blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Refresh token required',
                        'details': {}
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid or expired token',
                    'details': {'token': [str(e)]}
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'Logout failed',
                    'details': {'error': [str(e)]}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
