from django.contrib.auth.models import User, Group
from rest_framework import serializers
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory
from drf_hal_json.serializers import HalModelSerializer

"""
TODO:
- Program actual rating for movie
- Make a proper timestamp format for comments (00:00:00)
"""

"""
USER SERIALIZER - HalModelSerializer

Serializers allow complex data such as querysets and model instances to be
converted to native Python datatypes that can then be easily rendered into JSON,
XML or other content types. Serializers also provide deserialization, allowing
parsed data to be converted back into complex types, after first validating the
incoming data. - https://www.django-rest-framework.org/api-guide/serializers/
"""
class UserSerializer(HalModelSerializer):
    # Because 'reviews' is a reverse relationship on the User model, it will not be included by default when using the HalModelSerializer class, so we needed to add an explicit field for it.
    reviews = serializers.HyperlinkedRelatedField(many=True, view_name='review-detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)
    actors = serializers.HyperlinkedRelatedField(many=True, view_name='actor-detail', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'reviews', 'comments', 'actors')


"""
GROUP SERIALIZER (NOT IMPLEMENTED) - HalModelSerializer
"""
class GroupSerializer(HalModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


"""
MOVIE SERIALIZER - HalModelSerializer
"""
class MovieSerializer(HalModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)
    length = serializers.CharField(required=False, allow_blank=True, max_length=10)

    # TODO: Program average rating from reviews
    rating = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('title', 'length', 'rating', 'categories', 'actors')

    def display_value(self, instance):
        return 'Movie: %s' % (instance.title)


"""
REVIEW SERIALIZER - HalModelSerializer
"""
class ReviewSerializer(HalModelSerializer):
    text = serializers.CharField(required=False, allow_blank=True, max_length=3000)
    rating = serializers.IntegerField(required=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ('text', 'rating', 'author', 'movie')


"""
COMMENT SERIALIZER - HalModelSerializer
"""
class CommentSerializer(HalModelSerializer):
    text = serializers.CharField(required=False, allow_blank=True, max_length=400)
    # TODO: Make a proper timestamp format (00:00:00)
    timestamp = serializers.CharField(required=False, allow_blank=True, max_length=30)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('text', 'timestamp', 'author', 'movie')


"""
ACTOR SERIALIZER - HalModelSerializer
"""
class ActorSerializer(HalModelSerializer):
    firstname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Actor
        fields = ('firstname', 'lastname', 'author')


"""
CATEGORY SERIALIZER - HalModelSerializer
"""
class CategorySerializer(HalModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Category
        fields = ('name',)


"""
TRAILER SERIALIZER (NOT IMPLEMENTED) - HalModelSerializer
"""
class TrailerSerializer(HalModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    video_path = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        model = Trailer
        fields = ('video_path', 'author', 'movie')


"""
MOVIE-ACTOR SERIALIZER (NOT IMPLEMENTED) - HyperlinkedModelSerializer
"""
class MovieActorSerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()
    queryset_actor = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    related_actor = serializers.HyperlinkedRelatedField(
        queryset=queryset_actor,
        view_name='actor-detail'
    )
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='actor-detail'
    )

    class Meta:
        model = MovieActor
        fields = ('actor', 'movie')


"""
MOVIE-CATEGORY SERIALIZER (NOT IMPLEMENTED) - HyperlinkedModelSerializer
"""
class MovieCategorySerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    related_category = serializers.ReadOnlyField(source='category.name')
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='actor-detail'
    )

    class Meta:
        model = MovieCategory
        fields = ('related_category', 'related_movie')
