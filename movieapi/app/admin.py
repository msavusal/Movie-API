from django.contrib import admin
from movieapi.app.models import Movie, Review, Comment, Actor, Category

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Actor)
admin.site.register(Category)
