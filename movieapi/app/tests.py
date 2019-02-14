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
        Review.objects.create(title="TestReview", length="00:05:33", rating="5")

    def test_object_creation(self):
        print("Testing object creation for object Review")
        testReview = Review.objects.get(title="TestReview")
        self.assertEqual(testReview.title, 'TestReview')
