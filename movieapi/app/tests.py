from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from movieapi.app.models import Movie, Review, Comment, Actor, MovieActor, Trailer, Category, MovieCategory

"""
Test case for Movie model
"""
class MovieTestCase(APITestCase):
    print("==============================================")
    print("Tests for Movie model")
    print("==============================================")

    url = reverse('movie-list')

    def setUp(self):
        print("\n")

    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Movie")
        Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
        testMovie = Movie.objects.get(title="TestMovie")

        try:
            self.assertEqual(testMovie.title, 'TestMovie')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_get(self):
        print("Testing GET method for model Movie")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Movie")

        data = {
                "title":"TestMovie",
                "length":"01:45:44",
                "rating":"5",
                "related_categories": [],
                "related_actors": []
        }

        response = self.client.post(self.url, data, format='json')


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
