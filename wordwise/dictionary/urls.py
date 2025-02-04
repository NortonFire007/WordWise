from django.urls import path
from .views import WordListView, WordDetailView

urlpatterns = [
    path('dictionary/', WordListView.as_view(), name='word-list'),
    path('dictionary/<slug:slug>/', WordDetailView.as_view(), name='word-detail'),
]
