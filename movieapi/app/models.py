from django.db import models

# Create your models here.

"""
TODO:
- Comment
- Add all the models
"""

class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=3000, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Actor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Trailer(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)
