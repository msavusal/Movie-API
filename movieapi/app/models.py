from django.db import models


"""
Category model
"""
class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


"""
Actor model
"""
class Actor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', related_name='actors', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


"""
Movie model
"""
class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default='untitled')
    length = models.CharField(max_length=10, blank=True, default='00:00:00')
    rating = models.IntegerField(blank=True, default=0)
    categories = models.ManyToManyField(Category)
    actors = models.ManyToManyField(Actor)

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute

    # String constructor
    def __str__(self):
        return self.title


"""
Review model
"""
class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000, blank=True, default='')
    rating = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


"""
Comment model
"""
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.CharField(max_length=400, blank=True, default='')
    timestamp = models.CharField(max_length=10, blank=True, default='00:00:00')

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


"""
Trailer model
"""
class Trailer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', related_name='trailers', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    video_path = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


"""
Intermediate models
"""
class MovieCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    related_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    related_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute


class MovieActor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    related_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    related_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)     # Ordering elements based on "created" attribute
