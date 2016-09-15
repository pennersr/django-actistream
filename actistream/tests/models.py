from django.db import models
from django.utils import timezone


class Article(models.Model):
    pass


class Comment(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey('auth.User')
    timestamp = models.DateTimeField(default=timezone.now)
