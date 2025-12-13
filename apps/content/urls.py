from django.urls import path
from .views import ContentGenerateView, ContentHistoryView

urlpatterns = [
    path('generate/', ContentGenerateView.as_view(), name='content_generate'),
    path('history/', ContentHistoryView.as_view(), name='content_history'),
]
