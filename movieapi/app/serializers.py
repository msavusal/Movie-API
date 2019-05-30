from django.contrib.auth.models import User
from rest_framework import serializers
from movieapi.app.models import Movie, Review, Comment, Actor, Category
from drf_hal_json.serializers import HalModelSerializer



class UserSerializer(HalModelSerializer):
    """
    USER SERIALIZER - HalModelSerializer

    Serializers allow complex data such as querysets and model instances to be
    converted to native Python datatypes that can then be easily rendered into JSON,
    XML or other content types. Serializers also provide deserialization, allowing
    parsed data to be converted back into complex types, after first validating the
    incoming data. - https://www.django-rest-framework.org/api-guide/serializers/
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'reviews', 'comments', 'actors')


class MovieSerializer(HalModelSerializer):
    """
    MOVIE SERIALIZER - HalModelSerializer
    """
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)
    length = serializers.CharField(required=False, allow_blank=True, max_length=10)

    # TODO: Program average rating from reviews
    rating = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('title', 'length', 'rating', 'categories', 'actors')


class ReviewSerializer(HalModelSerializer):
    """
    REVIEW SERIALIZER - HalModelSerializer
    """
    text = serializers.CharField(required=False, allow_blank=True, max_length=3000)
    rating = serializers.IntegerField(required=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ('text', 'rating', 'author', 'movie')


class CommentSerializer(HalModelSerializer):
    """
    COMMENT SERIALIZER - HalModelSerializer
    """
    text = serializers.CharField(required=False, allow_blank=True, max_length=400)
    # TODO: Make a proper timestamp format (00:00:00)
    timestamp = serializers.CharField(required=False, allow_blank=True, max_length=30)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('text', 'timestamp', 'author', 'movie')


class ActorSerializer(HalModelSerializer):
    """
    ACTOR SERIALIZER - HalModelSerializer
    """
    firstname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Actor
        fields = ('firstname', 'lastname', 'author')


class CategorySerializer(HalModelSerializer):
    """
    CATEGORY SERIALIZER - HalModelSerializer
    """
    class Meta:
        model = Category
        fields = ('name',)
