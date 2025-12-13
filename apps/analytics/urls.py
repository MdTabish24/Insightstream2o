from django.urls import path
from .views import OutlierView, UploadStreakView, ThumbnailSearchView

urlpatterns = [
    path('outlier/', OutlierView.as_view(), name='outlier'),
    path('upload-streak/', UploadStreakView.as_view(), name='upload_streak'),
    path('thumbnail-search/', ThumbnailSearchView.as_view(), name='thumbnail_search'),
]
