from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions

from movieapi.app.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User, Group
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory
from movieapi.app.serializers import UserSerializer, GroupSerializer, MovieSerializer, ReviewSerializer, CommentSerializer, ActorSerializer, MovieActorSerializer, TrailerSerializer, CategorySerializer, MovieCategorySerializer

"""
TODO:
- Comment
- Add all the models
- Remove unused imports
"""

"""
MAIN VIEW
"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
        'actors': reverse('actor-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'movies': reverse('movie-list', request=request, format=format)
    })


"""
USER
"""
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
GROUP
"""
class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


"""
MOVIE
"""
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


"""
REVIEW
"""
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    #Override perform_create
    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


"""
COMMENT
"""
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


"""
ACTOR
"""
class ActorList(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


"""
MOVIEACTOR
"""
class MovieActorList(generics.ListCreateAPIView):
    queryset = MovieActor.objects.all()
    serializer_class = MovieActorSerializer


class MovieActorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieActor.objects.all()
    serializer_class = MovieActorSerializer


"""
TRAILER
"""
class TrailerList(generics.ListCreateAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class TrailerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer


"""
CATEGORY
"""
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
MOVIECATEGORY
"""
class MovieCategoryList(generics.ListCreateAPIView):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer


class MovieCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer
