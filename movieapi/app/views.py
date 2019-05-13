import operator
from django.shortcuts import render

from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q

from movieapi.app.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from movieapi.app.models import Movie, Review, Comment, Actor, Category
from movieapi.app.serializers import UserSerializer, MovieSerializer, ReviewSerializer, CommentSerializer, ActorSerializer, CategorySerializer
from drf_hal_json.views import HalCreateModelMixin


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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserDetailActorsList(generics.ListCreateAPIView):
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        serializer.save(author=self.request.user)
        serializer.save(user=user)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Actor.objects.filter(author=author) # Get the related actors to the user
        return queryset

class UserDetailReviewsList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        serializer.save(author=self.request.user)
        serializer.save(user=user)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Review.objects.filter(author=author) # Get the related reviews to the user
        return queryset

class UserDetailCommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        serializer.save(author=self.request.user)
        serializer.save(user=user)

    # Override queryset function
    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs[self.lookup_field]) # Get user by id (pk from context)
        queryset = Comment.objects.filter(author=author) # Get the related comments to the user
        return queryset


"""
MOVIE - Class-based views
"""
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class MovieDetailCategoriesList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Category.objects.filter(movie=movie) # Get the related categories to the movie
        return queryset

class MovieDetailActorsList(generics.ListCreateAPIView):
    serializer_class = ActorSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)
        serializer.save(movie=movie)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Actor.objects.filter(movie=movie) # Get the related actors to the movie
        return queryset

class MovieDetailReviewsList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)
        serializer.save(movie=movie)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Review.objects.filter(movie=movie) # Get the related reviews to the movie
        return queryset

class MovieDetailReviewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # Override get function
    def get(self, request, pk=None, pk2=None, format=None):
        filter = {'movie__id': pk2, 'pk': pk} # Construct lookup filter to use both movie_id and review_id
        review = get_object_or_404(Review, **filter) # Get object using the filter
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)

class MovieDetailCommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Override perform_create
    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)
        serializer.save(movie=movie)

    # Override queryset function
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs[self.lookup_field]) # Get movie by id (pk from context)
        queryset = Comment.objects.filter(movie=movie) # Get the related comments to the movie
        return queryset

class MovieDetailCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

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
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)

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
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)

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
        author = self.request.user
        if self.request.user.is_authenticated:
            serializer.save(author=author)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MovieSearchListView(MovieList):
    """
    Display a Movie List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(MovieSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(content__icontains=q) for q in query_list))
            )

        return result


"""
TEMPLATES (HTML)
"""
def index(request):
    """View function for main page of site."""

    # Populate the context
    context = {
        'version': 0.1,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def MovieSearchListView(request):
    """View function for search page for movies."""

    query = request.GET.get('q')
    movies = None
    q = None

    # Partial sentence match (Source: dani herrera, https://stackoverflow.com/questions/11594010/django-text-search-with-partial-sentence-match)
    if query:
        for word in query.split():
            q_aux = Q( title__icontains = word )
            q = ( q_aux & q ) if bool( q ) else q_aux
            movies = Movie.objects.filter(q)
    else:
        movies = Movie.objects.all()
        query = ""

    # Populate the context
    context = {
        'query': query,
        'movies': movies
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'movie_search_list_view.html', context=context)


def MovieDetailView(request, pk):
    """View function for Movie Detail page."""

    # Check if id is available
    if pk:
        movie = Movie.objects.get(id=pk)
        reviews = Review.objects.filter(movie=movie) # Get the related reviews to the movie

    # Populate the context
    context = {
        'movie': movie,
        'reviews': reviews
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'movie_detail.html', context=context)


def ActorDetailView(request, pk):
    """View function for Actor Detail page."""

    # Check if id is available
    if pk:
        actor = Actor.objects.get(id=pk)
        movies = Movie.objects.filter(actors=actor) # Get the related movies to this actor

    # Populate the context
    context = {
        'actor': actor,
        'movies': movies
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'actor_detail.html', context=context)


def CategoryDetailView(request, pk):
    """View function for Category Detail page."""

    # Check if id is available
    if pk:
        category = Category.objects.get(id=pk)
        movies = Movie.objects.filter(categories=category) # Get the related movies to this category

    # Populate the context
    context = {
        'category': category,
        'movies': movies
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'category_detail.html', context=context)
