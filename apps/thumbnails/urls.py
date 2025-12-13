from django.urls import path
from .views import ThumbnailGenerateView, ThumbnailHistoryView

urlpatterns = [
    path('generate/', ThumbnailGenerateView.as_view(), name='thumbnail_generate'),
    path('history/', ThumbnailHistoryView.as_view(), name='thumbnail_history'),
]
