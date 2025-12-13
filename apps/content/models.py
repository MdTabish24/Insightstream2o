from django.db import models
from django.conf import settings

class AIContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_contents')
    user_input = models.CharField(max_length=500)
    content = models.JSONField()
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.user_input[:50]}"
