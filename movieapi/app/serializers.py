from django.contrib.auth.models import User, Group
from rest_framework import serializers
from movieapi.app.models import Movie, Review

"""
TODO:
- Comment
- Add all the models
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #Because 'reviews' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it.
    reviews = serializers.HyperlinkedRelatedField(many=True, view_name='review-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'reviews')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)

    """
    This is the manual way to define create and update functions
    def create(self, validated_data):

        #Create and return a new `Movie` instance, given the validated data.
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):

        #Update and return an existing `Movie` instance, given the validated data.
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
    """

    class Meta:
        model = Movie
        fields = ('id', 'title')


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True, max_length=200)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'owner')
