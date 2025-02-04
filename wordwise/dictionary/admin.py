from django.contrib import admin
from .models import Word, Meaning, Sound, Example, Phrase, Cognate


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'slug', 'level', 'rank')
    list_filter = ('level',)
    search_fields = ('text', 'description')
    prepopulated_fields = {'slug': ('text',)}


@admin.register(Meaning)
class MeaningAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition', 'part_of_speech')
    list_filter = ('part_of_speech',)
    search_fields = ('definition',)


@admin.register(Sound)
class SoundAdmin(admin.ModelAdmin):
    list_display = ('word', 'sound', 'transcription', 'region')
    search_fields = ('region',)


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('word', 'text')
    search_fields = ('text',)


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ( 'word', 'phrase_text')
    search_fields = ('phrase_text',)


@admin.register(Cognate)
class CognateAdmin(admin.ModelAdmin):
    list_display = ('word', 'related_word')
    search_fields = ('word__text', 'related_word')
