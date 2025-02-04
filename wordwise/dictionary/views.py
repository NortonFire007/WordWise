from rest_framework import generics
from .models import Word
from .serializers import WordSerializer

class WordListView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class WordDetailView(generics.RetrieveAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'slug'