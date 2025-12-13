from django.urls import path
from .views import KeywordResearchView

urlpatterns = [
    path('research/', KeywordResearchView.as_view(), name='keyword_research'),
]
