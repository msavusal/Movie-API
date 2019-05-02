from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from movieapi.app.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User, Group
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory
from movieapi.app.serializers import UserSerializer, GroupSerializer, MovieSerializer, ReviewSerializer, CommentSerializer, ActorSerializer, MovieActorSerializer, TrailerSerializer, CategorySerializer, MovieCategorySerializer
from drf_hal_json.views import HalCreateModelMixin

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
USER - Class-based views
"""
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

class UserDetailActorsList(generics.ListAPIView):
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Actor.objects.filter(author=author) # Get the related actors to the user
        return queryset

class UserDetailReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Review.objects.filter(author=author) # Get the related reviews to the user
        return queryset

class UserDetailCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Comment.objects.filter(author=author) # Get the related comments to the user
        return queryset


"""
GROUP (NOT IMPLEMENTED) - Class-based views
"""
class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


"""
MOVIE - Class-based views
"""
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailCategoriesList(generics.ListAPIView):
    serializer_class = CategorySerializer

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Category.objects.filter(movie=movie) # Get the related categories to the movie
        return queryset

class MovieDetailActorsList(generics.ListAPIView):
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Actor.objects.filter(movie=movie) # Get the related actors to the movie
        return queryset

class MovieDetailReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Review.objects.filter(movie=movie) # Get the related reviews to the movie
        return queryset

class MovieDetailReviewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # Override get function
    def get(self, request, pk=None, pk2=None, format=None):
        filter = {'movie__id': pk2, 'pk': pk} # Construct lookup filter to use both movie_id and review_id
        review = get_object_or_404(Review, **filter) # Get object using the filter
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)

class MovieDetailCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Comment.objects.filter(movie=movie) # Get the related comments to the movie
        return queryset

class MovieDetailCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # Override get function
    def get(self, request, pk=None, pk2=None, format=None):
        filter = {'movie__id': pk2, 'pk': pk} # Construct lookup filter to use both movie_id and comment_id
        comment = get_object_or_404(Comment, **filter) # Get object using the filter
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)


"""
REVIEW - Class-based views
"""
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


"""
COMMENT - Class-based views
"""
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


"""
ACTOR - Class-based views
"""
class ActorList(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


"""
CATEGORY - Class-based views
"""
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
TRAILER (NOT IMPLEMENTED) - Class-based views
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
MOVIECATEGORY (NOT IMPLEMENTED) - Class-based views
"""
class MovieCategoryList(generics.ListCreateAPIView):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer


class MovieCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer


"""
MOVIEACTOR (NOT IMPLEMENTED) - Class-based views
"""
class MovieActorList(generics.ListCreateAPIView):
    queryset = MovieActor.objects.all()
    serializer_class = MovieActorSerializer


class MovieActorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieActor.objects.all()
    serializer_class = MovieActorSerializer


"""
TEMPLATES
"""
def index(request):
    """View function for home page of site."""

    context = {
        'version': 0.1,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
