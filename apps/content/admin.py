from django.contrib import admin
from .models import AIContent

@admin.register(AIContent)
class AIContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user_input', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user_input']
    ordering = ['-created_at']
    raw_id_fields = ['user']
