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
class ReviewTestCase(APITestCase):
    print("==============================================")
    print("Tests for Review model")
    print("==============================================")
    
    url = reverse('movie-list')

    def setUp(self):
        print("\n")
        
    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Review")
        Review.objects.create(text="Excellent movie.", rating=5)
        testReview = Review.objects.get(title="TestReview")
        
        try:
            self.assertEqual(testReview.title, 'TestReview')
            print("SUCCESS")
        except:
            print("FAILED")
            
    # Test GET method
    def test_get(self):
        print("Testing GET method for model Review")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Review")

        data = {
                "title":"TestReview",
                "text":"Excellent movie.",
                "rating":"5",
                "related_user": [],
                "related_movie": []
        }

        response = self.client.post(self.url, data, format='json')


"""
Test case for Comment model
"""
class CommentTestCase(APITestCase):
    print("==============================================")
    print("Tests for Comment model")
    print("==============================================")

    url = reverse('movie-list')

    def setUp(self):
        print("\n")

    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Comment")
        Comment.objects.create(text="It was okay.", timestamp="00:00:00")
        testComment = Comment.objects.get(title="TestComment")
        try:
            self.assertEqual(testComment.title, 'TestComment')
            print("SUCCESS")
        except:
            print("FAILED")
            
    # Test GET method
    def test_get(self):
        print("Testing GET method for model Comment")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Comment")

        data = {
                "title":"TestComment",
                "text":"It was okay.",
                "timestamp":"00:00:00",
                "related_user": [],
                "related_movie": []
        }

        response = self.client.post(self.url, data, format='json')


"""
Test case for Actor model
"""
class ActorTestCase(APITestCase):
    print("==============================================")
    print("Tests for Actor model")
    print("==============================================")

    url = reverse('movie-list')

    def setUp(self):
        print("\n")

    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Actor")
        Actor.objects.create(firstname="John", lastname= "Doe")
        testActor = Actor.objects.get(title="TestActor")
        
        try:
            self.assertEqual(testActor.title, 'TestActor')
            print("SUCCESS")
        except:
            print("FAILED")
            
    # Test GET method
    def test_get(self):
        print("Testing GET method for model Actor")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Actor")

        data = {
                "firstname":"John",
                "lastname":"Doe",
                "related_user": [],
        }

        response = self.client.post(self.url, data, format='json')


"""
Test case for Trailer model
"""
class TrailerTestCase(APITestCase):
    print("==============================================")
    print("Tests for Trailer model")
    print("==============================================")

    url = reverse('movie-list')

    def setUp(self):
        print("\n")

    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Trailer")
        Trailer.objects.create(video_path="VIDEO_PATH")
        testTrailer = Trailer.objects.get(title="TestTrailer")
        
        try:
            self.assertEqual(testTrailer.title, 'TestTrailer')
            print("SUCCESS")
        except:
            print("FAILED")
            
    # Test GET method
    def test_get(self):
        print("Testing GET method for model Trailer")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Trailer")

        data = {
                "video_path":"VIDEO_PATH",
                "related_user": [],
                "related_movie": []
        }

        response = self.client.post(self.url, data, format='json')

        
"""
Test case for Category model
"""
class CategoryTestCase(APITestCase):
    print("==============================================")
    print("Tests for Category model")
    print("==============================================")

    url = reverse('movie-list')

    def setUp(self):
        print("\n")

    # Test object creation
    def test_object_creation(self):
        print("Testing object creation for object Category")
        Category.objects.create(name="Action")
        testCategory = Category.objects.get(title="TestCategory")

        try:
            self.assertEqual(testCategory.title, 'TestCategory')
            print("SUCCESS")
        except:
            print("FAILED")
            
    # Test GET method
    def test_get(self):
        print("Testing GET method for model Category")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_post(self):
        print("Testing POST method for model Category")

        data = {
                "name":"Action"
        }

        response = self.client.post(self.url, data, format='json')
