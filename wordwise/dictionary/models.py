import os
from django.db import models
from django.urls import reverse
from slugify import slugify

LEVEL_CHOICES = [
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('C1', 'C1'),
    ('C2', 'C2'),
]

PART_OF_SPEECH_CHOICES = [
    ('adjectival', 'adjectival'),
    ('noun', 'noun'),
    ('verb', 'verb'),
    ('alliance', 'alliance'),
    ('adverb', 'adverb'),
    ('pronoun', 'pronoun'),
    ('other', 'other'),
    ('pretext', 'pretext'),
    ('interjection', 'interjection'),
    ('article', 'article'),
    ('irregular verb', 'irregular verb'),
    ('phrasal_verb', 'phrasal verb'),
]


def sound_upload_path(instance, filename):
    """
    Files are stored in 'sounds/<word_slug>/<filename>'.
    """
    return os.path.join('sounds', instance.word.slug, filename)


class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)
    rank = models.PositiveIntegerField(default=22000, blank=True, null=True)
    synonyms = models.ManyToManyField('self', blank=True, symmetrical=True)
    related_phrasal_verbs = models.ManyToManyField('self',
                                                   blank=True,
                                                   symmetrical=False,
                                                   related_name='related_words')

    class Meta:
        ordering = ['text', 'rank']
        verbose_name = 'Word'
        verbose_name_plural = 'Words'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('word-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.text


class Meaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='meanings')
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH_CHOICES)
    definition = models.TextField()
    translations = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Meaning'
        verbose_name_plural = 'Meanings'

    def __str__(self):
        return f'{self.word.text} ({self.part_of_speech})'


class Sound(models.Model):
    word = models.ForeignKey(Word, related_name='sounds', on_delete=models.CASCADE)
    region = models.CharField(choices=[
        ('UK', 'United Kingdom'),
        ('US', 'United States')
    ], verbose_name='region', max_length=50)
    transcription = models.CharField(max_length=255, blank=True, null=True)
    sound = models.FileField(upload_to=sound_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Sound'
        verbose_name_plural = 'Sounds'

    def __str__(self):
        return f'{self.word.text} - {self.region}'


class Example(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='examples')
    text = models.TextField()
    translations = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'

    def __str__(self):
        return f'Example for {self.word.text}'


class Phrase(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='phrases')
    phrase_text = models.CharField(max_length=255)
    translations = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Phrase'
        verbose_name_plural = 'Phrases'

    def __str__(self):
        return f'Phrase: {self.phrase_text}'


class Cognate(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='cognates')
    related_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Cognate'
        verbose_name_plural = 'Cognates'

    def __str__(self):
        return f'Cognate: {self.related_word} for {self.word.text}'
