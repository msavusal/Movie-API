from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User, Group
from movieapi.app.models import Movie, Review, Comment, Actor, Trailer, Category
from movieapi.app import views


"""
Test case for Movie model
"""
class MovieTestCase(APITestCase):
    url = reverse('movie-list')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Movie")
        Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
        testMovie = Movie.objects.get(title="TestMovie")

        try:
            self.assertEqual(testMovie.title, 'TestMovie')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Movie")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Movie")

        data = {
            "title":"TestMovie",
            "length":"01:45:44",
            "rating":"5",
            "related_categories": [],
            "related_actors": []
        }

        response = self.client.post(self.url, data, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Movie.objects.count(), 1)
            self.assertEqual(Movie.objects.get().title, 'TestMovie')
            print("SUCCESS")
        except:
            print("FAILED")


"""
Test case for Review model
"""
class ReviewTestCase(APITestCase):
    url = reverse('review-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Review")
        Review.objects.create(text="Excellent movie.", rating=5, related_movie_id=1, related_user_id=1)
        testReview = Review.objects.get(text="Excellent movie.")

        try:
            self.assertEqual(testReview.text, 'Excellent movie.')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Review")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Review")

        data = {
            "text":"Excellent movie.",
            "rating":5,
            "related_movie_id":1,
            "related_actor_id":1
        }

        # Create requrest
        request = self.factory.post(self.url, data, format="json")

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ReviewList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Review.objects.count(), 1)
            self.assertEqual(Review.objects.get().text, 'Excellent movie.')
            print("SUCCESS")
        except:
            print("FAILED")


"""
Test case for Comment model
"""
class CommentTestCase(APITestCase):
    url = reverse('comment-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Comment")
        Comment.objects.create(text="It was okay.", timestamp="00:00:00", related_movie_id=1, related_user_id=1)
        testComment = Comment.objects.get(text="It was okay.")
        try:
            self.assertEqual(testComment.text, 'It was okay.')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Comment")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Comment")

        data = {
            "title":"TestComment",
            "text":"It was okay.",
            "timestamp":"00:00:00",
            "related_user": 1,
            "related_movie": 1
        }

        # Create requrest
        request = self.factory.post(self.url, data, format="json")

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.CommentList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(Comment.objects.get().text, 'It was okay.')
            print("SUCCESS")
        except:
            print("FAILED")


"""
Test case for Actor model
"""
class ActorTestCase(APITestCase):
    url = reverse('actor-list')

    user = User.objects.get(id=1)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Actor")
        Actor.objects.create(firstname="John", lastname= "Doe", related_user=self.user)
        testActor = Actor.objects.get(firstname="John")

        try:
            self.assertEqual(testActor.firstname, 'John')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Actor")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Actor")

        data = {
            "firstname":"John",
            "lastname":"Doe",
        }

        # Create requrest
        request = self.factory.post(self.url, data, format="json")

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ActorList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Actor.objects.count(), 1)
            self.assertEqual(Actor.objects.get().firstname, 'John')
            print("SUCCESS")
        except:
            print("FAILED")


"""
Test case for Trailer model
"""
class TrailerTestCase(APITestCase):
    url = reverse('trailer-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Trailer")
        Trailer.objects.create(video_path="VIDEO_PATH", related_movie_id=1, related_user_id=1)
        testTrailer = Trailer.objects.get(video_path="VIDEO_PATH")

        try:
            self.assertEqual(testTrailer.video_path, 'VIDEO_PATH')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Trailer")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Trailer")

        data = {
            "video_path":"VIDEO_PATH",
            "related_user": 1,
            "related_movie": 1
        }

        # Create requrest
        request = self.factory.post(self.url, data, format="json")

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ActorList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Trailer.objects.count(), 1)
            self.assertEqual(Trailer.objects.get().video_path, 'VIDEO_PATH')
            print("SUCCESS")
        except:
            print("FAILED")


"""
Test case for Category model
"""
class CategoryTestCase(APITestCase):
    url = reverse('category-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Category")
        Category.objects.create(name="TestCategory")
        testCategory = Category.objects.get(name="TestCategory")

        try:
            self.assertEqual(testCategory.name, 'TestCategory')
            print("SUCCESS")
        except:
            print("FAILED")

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Category")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Category")

        data = {
            "name":"Action"
        }

        response = self.client.post(self.url, data, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Category.objects.count(), 1)
            self.assertEqual(Category.objects.get().name, 'Action')
            print("SUCCESS")
        except:
            print("FAILED")
