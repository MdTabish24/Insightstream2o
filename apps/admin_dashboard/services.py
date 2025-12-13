from django.conf import settings
from django.db.models import Count
from apps.users.models import User
from apps.thumbnails.models import Thumbnail
from apps.content.models import AIContent

class AdminService:
    def authenticate(self, username: str, password: str) -> bool:
        return username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD
    
    def get_stats(self) -> dict:
        total_users = User.objects.count()
        total_thumbnails = Thumbnail.objects.count()
        total_content = AIContent.objects.count()
        
        most_active = User.objects.annotate(
            thumbnail_count=Count('thumbnails'),
            content_count=Count('ai_contents')
        ).order_by('-thumbnail_count', '-content_count')[:5]
        
        recent_users = User.objects.order_by('-created_at')[:10]
        
        return {
            'total_users': total_users,
            'total_thumbnails': total_thumbnails,
            'total_content': total_content,
            'most_active_users': [{'email': u.email, 'thumbnails': u.thumbnail_count, 'content': u.content_count} for u in most_active],
            'recent_registrations': [{'email': u.email, 'created_at': u.created_at.isoformat()} for u in recent_users]
        }
