from rest_framework import serializers
from .models import Word, Meaning, Sound, Example, Phrase, Cognate


class MeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['id', 'part_of_speech', 'definition', 'translations']


class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ['id', 'region', 'transcription', 'sound']


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'text', 'translations']


class PhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = ['id', 'phrase_text', 'translations']


class CognateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cognate
        fields = ['id', 'related_word']


class WordSerializer(serializers.ModelSerializer):
    meanings = MeaningSerializer(many=True, read_only=True)
    sounds = SoundSerializer(many=True, read_only=True)
    examples = ExampleSerializer(many=True, read_only=True)
    phrases = PhraseSerializer(many=True, read_only=True)
    cognates = CognateSerializer(many=True, read_only=True)
    synonyms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    related_phrasal_verbs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Word
        fields = [
            'id', 'text', 'slug', 'description', 'level', 'rank',
            'meanings', 'sounds', 'examples', 'phrases', 'cognates',
            'synonyms', 'related_phrasal_verbs'
        ]
