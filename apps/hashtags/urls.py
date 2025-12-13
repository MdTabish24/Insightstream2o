from django.urls import path
from .views import HashtagGenerateView

urlpatterns = [
    path('generate/', HashtagGenerateView.as_view(), name='hashtag_generate'),
]
