from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserService:
    @staticmethod
    def create_user(email: str, username: str, password: str) -> User:
        """Create a new user with hashed password"""
        return User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
    
    @staticmethod
    def generate_tokens(user: User) -> dict:
        """Generate JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    @staticmethod
    def blacklist_token(refresh_token: str) -> None:
        """Blacklist a refresh token"""
        token = RefreshToken(refresh_token)
        token.blacklist()
    
    @staticmethod
    def get_user_by_email(email: str) -> User:
        """Get user by email"""
        return User.objects.get(email=email)
    
    @staticmethod
    def email_exists(email: str) -> bool:
        """Check if email already exists"""
        return User.objects.filter(email=email).exists()

user_service = UserService()
