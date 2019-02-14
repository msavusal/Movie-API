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
        Review.objects.create(text="Excellent movie.", rating=5)

    def test_object_creation(self):
        print("Testing object creation for object Review")
        testReview = Review.objects.get(title="TestReview")
        self.assertEqual(testReview.title, 'TestReview')
        
"""
Test case for Comment model
"""
class CommentTestCase(TestCase):
    def setUp(self):
        Comment.objects.create(text="It was okay.", timestamp="00:00:00")

    def test_object_creation(self):
        print("Testing object creation for object Comment")
        testComment = Comment.objects.get(title="TestComment")
        self.assertEqual(testComment.title, 'TestComment')
        
"""
Test case for Actor model
"""
class ActorTestCase(TestCase):
    def setUp(self):
        Actor.objects.create(firstname="John", lastname= "Doe")

    def test_object_creation(self):
        print("Testing object creation for object Actor")
        testActor = Actor.objects.get(title="TestActor")
        self.assertEqual(testActor.title, 'TestActor')


"""
Test case for Trailer model
"""
class TrailerTestCase(TestCase):
    def setUp(self):
        Trailer.objects.create(video_path="VIDEO_PATH")

    def test_object_creation(self):
        print("Testing object creation for object Trailer")
        testTrailer = Trailer.objects.get(title="TestTrailer")
        self.assertEqual(testTrailer.title, 'TestTrailer')
        
"""
Test case for Category model
"""
class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Action")

    def test_object_creation(self):
        print("Testing object creation for object Category")
        testCategory = Category.objects.get(title="TestCategory")
        self.assertEqual(testCategory.title, 'TestCategory')

        
