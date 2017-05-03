from django.db import models
from django.utils import timezone


class Article(models.Model):
    pass


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
