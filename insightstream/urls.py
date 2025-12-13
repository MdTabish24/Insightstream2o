from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'InsightStream API',
        'version': '1.0',
        'endpoints': {
            'users': '/api/users/',
            'thumbnails': '/api/thumbnails/',
            'content': '/api/content/',
            'keywords': '/api/keywords/',
            'hashtags': '/api/hashtags/',
            'analytics': '/api/analytics/',
            'admin': '/api/admin-dashboard/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/users/', include('apps.users.urls')),
    path('api/thumbnails/', include('apps.thumbnails.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/keywords/', include('apps.keywords.urls')),
    path('api/hashtags/', include('apps.hashtags.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/admin-dashboard/', include('apps.admin_dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve frontend - catch all other routes and serve index.html
# This allows React/Next.js routing to work
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='frontend'),
]
