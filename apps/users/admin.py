from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'created_at', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username']
    ordering = ['-created_at']
