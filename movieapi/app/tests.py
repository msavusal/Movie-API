from django.test import TestCase
from rest_framework.test import APIRequestFactory
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory

"""
Test case for Movie model
"""
class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="TestMovie", length="01:45:44", rating="5")

    def test_object_creation(self):
        print("Testing object creation for object Movie")
        testMovie = Movie.objects.get(title="TestMovie")
        self.assertEqual(testMovie.title, 'TestMovie')
        
"""
Test case for Review model
"""
class ReviewTestCase(TestCase):
    def setUp(self):
        Review.objects.create(title="TestReview", length="00:05:33", rating="3")

    def test_object_creation(self):
        print("Testing object creation for object Review")
        testReview = Review.objects.get(title="TestReview")
        self.assertEqual(testReview.title, 'TestReview')
        
"""
Test case for Comment model
"""
class CommentTestCase(TestCase):
    def setUp(self):
        Comment.objects.create(title="TestComment", length=21)

    def test_object_creation(self):
        print("Testing object creation for object Comment")
        testComment = Comment.objects.get(title="TestComment")
        self.assertEqual(testComment.title, 'TestComment')
        
"""
Test case for Actor model
"""
class ActorTestCase(TestCase):
    def setUp(self):
        Actor.objects.create(title="TestActor", name="John Doe", age=27)

    def test_object_creation(self):
        print("Testing object creation for object Actor")
        testActor = Actor.objects.get(title="TestActor")
        self.assertEqual(testActor.title, 'TestActor')
        
"""
Test case for MovieActor model
"""
class MovieActorTestCase(TestCase):
    def setUp(self):
        MovieActor.objects.create(title="TestMovieActor", name="John Doe", age=27)

    def test_object_creation(self):
        print("Testing object creation for object MovieActor")
        testMovie = MovieActor.objects.get(title="TestMovie")
        self.assertEqual(testMovie.title, 'TestMovie')

"""
Test case for Trailer model
"""
class TrailerTestCase(TestCase):
    def setUp(self):
        Trailer.objects.create(title="TestTrailer", length="00:02:11", rating="5")

    def test_object_creation(self):
        print("Testing object creation for object Trailer")
        testTrailer = Trailer.objects.get(title="TestTrailer")
        self.assertEqual(testTrailer.title, 'TestTrailer')        
