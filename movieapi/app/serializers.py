from django.contrib.auth.models import User, Group
from rest_framework import serializers
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory

"""
TODO:
- Comment
- Program actual rating for movie
- Make a proper timestamp format for comments (00:00:00)
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #Because 'reviews' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it.
    reviews = serializers.HyperlinkedRelatedField(many=True, view_name='review-detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)
    added_actors = serializers.HyperlinkedRelatedField(many=True, view_name='actor-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'reviews', 'comments', 'added_actors')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    queryset_categories = Category.objects.all()
    queryset_actors = Actor.objects.all()

    # id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)
    length = serializers.CharField(required=False, allow_blank=True, max_length=10)
    related_categories = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=queryset_categories,
        view_name='category-detail'
    )
    related_actors = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=queryset_actors,
        view_name='actor-detail'
    )

    # TODO: Program average rating from reviews
    rating = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'length', 'rating', 'related_categories', 'related_actors')

    def display_value(self, instance):
        return 'Movie: %s' % (instance.title)


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True, max_length=3000)
    rating = serializers.IntegerField(required=True)
    related_user = serializers.ReadOnlyField(source='related_user.username')
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='movie-detail'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'related_user', 'related_movie')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True, max_length=400)

    # TODO: Make a proper timestamp format (00:00:00)
    timestamp = serializers.CharField(required=False, allow_blank=True, max_length=30)

    related_user = serializers.ReadOnlyField(source='related_user.username')
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='movie-detail'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'timestamp', 'related_user', 'related_movie')


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    firstname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    related_user = serializers.ReadOnlyField(source='related_user.username')

    class Meta:
        model = Actor
        fields = ('id', 'firstname', 'lastname', 'related_user')


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
        fields = ('id', 'related_actor', 'related_movie')


class TrailerSerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    related_user = serializers.ReadOnlyField(source='related_user.username')
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='actor-detail'
    )
    video_path = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        model = Trailer
        fields = ('id', 'video_path', 'related_user', 'related_movie')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Category
        fields = ('id', 'name')


class MovieCategorySerializer(serializers.HyperlinkedModelSerializer):
    queryset_movie = Movie.objects.all()

    # id = serializers.IntegerField(read_only=True)
    related_category = serializers.ReadOnlyField(source='related_category.name')
    related_movie = serializers.HyperlinkedRelatedField(
        queryset=queryset_movie,
        view_name='actor-detail'
    )

    class Meta:
        model = MovieCategory
        fields = ('id', 'related_category', 'related_movie')
