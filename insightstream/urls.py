from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/thumbnails/', include('apps.thumbnails.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/keywords/', include('apps.keywords.urls')),
    path('api/hashtags/', include('apps.hashtags.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/admin-dashboard/', include('apps.admin_dashboard.urls')),
]
