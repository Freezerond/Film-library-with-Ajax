from django.db import models
import os
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from deep_translator import GoogleTranslator
from django.contrib.auth.models import User


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Данный формат файла не поддерживается')


class Movie(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    films = models.FileField(upload_to='films/', validators=[validate_file_extension])
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='movies', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        text = GoogleTranslator(source='ru', target='en').translate(self.title)
        self.slug = slugify(text.lower().replace(' ', '-'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        text = GoogleTranslator(source='ru', target='en').translate(self.title)
        self.slug = slugify(text.lower().replace(' ', '-'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class CommentMovie(models.Model):
    post = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta():
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class MovieVote(models.Model):
    VOTES = (
        (1, 'Like'),
        (-1, 'Dislike')
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    vote = models.SmallIntegerField(choices=VOTES)

    class Meta:
        unique_together = (('movie', 'user'),)
