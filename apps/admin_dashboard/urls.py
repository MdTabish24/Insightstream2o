from django.urls import path
from .views import AdminLoginView, AdminStatsView

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('stats/', AdminStatsView.as_view(), name='admin_stats'),
]
