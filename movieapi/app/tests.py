import json

from django import db as exception
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from movieapi.app.models import Movie, Review, Comment, Actor, Category
from movieapi.app import views

from drf_hal_json import LINKS_FIELD_NAME, EMBEDDED_FIELD_NAME


class MovieTestCase(APITestCase):
"""
Test case for Movie model
"""
    TESTSERVER_URL = "http://testserver"
    url = reverse('movie-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username='test_admin', email='test_admin@…', password='password')
        actorObject = Actor.objects.create(firstname="John", lastname= "Doe", author=self.user)
        categoryObject = Category.objects.create(name="TestCategory")

        self.actor_url = self.TESTSERVER_URL + reverse('actor-detail', kwargs={'pk': actorObject.id})
        self.category_url = self.TESTSERVER_URL + reverse('category-detail', kwargs={'pk': categoryObject.id})

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Movie")
        Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
        testMovie = Movie.objects.get(title="TestMovie")

        try:
            self.assertTrue(isinstance(testMovie, Movie))
            self.assertEqual(testMovie.title, 'TestMovie')
            self.assertEqual(str(testMovie), testMovie.title) # Test __str__ method
            print("SUCCESS")
        except:
            print("FAILED")

    # Test unique constraint
    def test_1_2_object_unique(self):
        print("Testing unique constraint for object Movie")

        Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")

        try:
            Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
            self.fail("FAILED")
            print("FAILED")
        except exception.IntegrityError:
            print("SUCCESS")
            pass

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Movie (expect 200)")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Movie (expect 201)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "categories": [self.category_url],
                "actors": [self.actor_url]
            },
            "title":"TestMovie",
            "length":"01:45:44",
            "rating":5
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Movie.objects.count(), 1)
            self.assertEqual(Movie.objects.get().title, 'TestMovie')
            self.assertEqual(Movie.objects.get().length, '01:45:44')
            self.assertEqual(Movie.objects.get().rating, 5)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test POST method with bad request
    def test_3_post_400(self):
        print("Testing POST method for model Movie with bad request (expect 400)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "categories": "FALSE LINK"
            },
            "title":"TestMovie",
            "length":"01:45:44",
            "rating":5
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ReviewList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method
    def test_4_delete(self):
        print("Testing DELETE method for model Movie (expect 204)")
        self.client.login(username='test_admin', password='password')

        testObject = Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")

        # Create response
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Movie.objects.count(), 0)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method without permission
    def test_4_delete_403(self):
        print("Testing DELETE method for model Movie without permission (expect 403)")
        self.client.logout()

        testObject = Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")

        # Create response
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test DELETE method on review that does not exist
    def test_4_delete_404(self):
        print("Testing DELETE method for model Movie that does not exist (expect 404)")
        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': 999}))

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test UPDATE method
    def test_5_update(self):
        print("Testing UPDATE method for model Movie (expect 200)")
        self.client.login(username='test_admin', password='password')

        testObject = Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")

        data = {
            "_links": {
                "url": self.TESTSERVER_URL + self.url + str(testObject.id),
                "categories": [self.category_url],
                "actors": [self.actor_url]
            },
            "title": "TestMovie CHANGED",
            "length": "01:44:34",
            "rating": 3
        }

        # Create response
        response = self.client.patch(reverse('movie-detail', kwargs={'pk': testObject.pk}), data=json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Movie.objects.get().title, 'TestMovie CHANGED')
            self.assertEqual(Movie.objects.get().length, '01:44:34')
            self.assertEqual(Movie.objects.get().rating, 3)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


class ReviewTestCase(APITestCase):
"""
Test case for Review model
"""
    TESTSERVER_URL = "http://testserver"
    url = reverse('review-list')

    # Set up factory, create user and movie objects and construct movie url for hyperlinking
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')
        self.movieObject = Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
        self.movie_url = self.TESTSERVER_URL + reverse('movie-detail', kwargs={'pk': self.movieObject.id})

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Review")
        Review.objects.create(text="Excellent movie.", rating=5, movie_id=1, author_id=1)
        testReview = Review.objects.get(text="Excellent movie.")

        try:
            self.assertTrue(isinstance(testReview, Review))
            self.assertEqual(testReview.text, 'Excellent movie.')
            self.assertEqual(str(testReview), "Review for " + self.movieObject.title) # Test __str__ method
            print("SUCCESS")
        except:
            print("FAILED")

    # Test unique constraint
    def test_1_2_object_unique(self):
        print("Testing unique constraint for object Review")

        Review.objects.create(id=1, text="Excellent movie.", rating=5, movie_id=1, author_id=1)

        try:
            Review.objects.create(id=1, text="Excellent movie.", rating=5, movie_id=1, author_id=1)
            self.fail("FAILED")
            print("FAILED")
        except exception.IntegrityError:
            print("SUCCESS")
            pass

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Review (expect 200)")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Review (expect 201)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "movie": self.movie_url
            },
            "text": "Excellent movie.",
            "rating": 5
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

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

        self.client.logout()

    # Test POST method with bad request
    def test_3_post_400(self):
        print("Testing POST method for model Review with bad request (expect 400)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "movie": "FALSE LINK"
            },
            "text": "Excellent movie.",
            "rating": 5
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ReviewList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


    # Test DELETE method
    def test_4_delete(self):
        print("Testing DELETE method for model Review (expect 204)")

        testObject = Review.objects.create(text="Excellent movie.", rating=5, movie_id=1, author_id=1)

        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('review-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Review.objects.count(), 0)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method without permission
    def test_4_delete_403(self):
        print("Testing DELETE method for model Review without permission (expect 403)")
        self.client.logout()

        testObject = Review.objects.create(text="Excellent movie.", rating=5, movie_id=1, author_id=1)

        # Create response
        response = self.client.delete(reverse('review-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test DELETE method on review that does not exist
    def test_4_delete_404(self):
        print("Testing DELETE method for model Review that does not exist (expect 404)")
        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('review-detail', kwargs={'pk': 999}))

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test UPDATE method
    def test_5_update(self):
        print("Testing UPDATE method for model Review (expect 200)")

        testObject = Review.objects.create(text="Excellent movie.", rating=5, movie_id=1, author_id=1)

        self.client.login(username='test_admin', password='password')

        data = {
            '_links': {
                'url': self.TESTSERVER_URL + self.url + str(testObject.id),
                'movie': self.movie_url
            },
            'text': "Excellent movie. CHANGED",
            'rating': 5
        }

        # Create response
        response = self.client.put(reverse('review-detail', kwargs={'pk': testObject.pk}), data=json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Review.objects.get().text, 'Excellent movie. CHANGED')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


class CommentTestCase(APITestCase):
"""
Test case for Comment model
"""
    TESTSERVER_URL = "http://testserver"
    url = reverse('comment-list')

    # Set up factory, create user and movie objects and construct movie url for hyperlinking
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')
        self.movieObject = Movie.objects.create(id=1, title="TestMovie", length="01:45:44", rating="5")
        self.movie_url = self.TESTSERVER_URL + reverse('movie-detail', kwargs={'pk': self.movieObject.id})

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Comment")
        Comment.objects.create(text="It was okay.", timestamp="00:00:00", movie_id=1, author_id=1)
        testComment = Comment.objects.get(text="It was okay.")

        try:
            self.assertTrue(isinstance(testComment, Comment))
            self.assertEqual(testComment.text, 'It was okay.')
            self.assertEqual(str(testComment), "Comment for " + self.movieObject.title) # Test __str__ method
            print("SUCCESS")
        except:
            print("FAILED")

    # Test unique constraint
    def test_1_2_object_unique(self):
        print("Testing unique constraint for object Comment")

        Comment.objects.create(id=1, text="It was okay.", timestamp="00:00:00", movie_id=1, author_id=1)

        try:
            Comment.objects.create(id=1, text="It was okay.", timestamp="00:00:00", movie_id=1, author_id=1)
            self.fail("FAILED")
            print("FAILED")
        except exception.IntegrityError:
            print("SUCCESS")
            pass

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Comment (expect 200)")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Comment (expect 201)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "movie": self.movie_url
            },
            "text": "Excellent movie.",
            "timestamp": "00:30:30"
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.CommentList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(Comment.objects.get().text, 'Excellent movie.')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test POST method with bad request
    def test_3_post_400(self):
        print("Testing POST method for model Comment with bad request (expect 400)")
        self.client.login(username='test_admin', password='password')

        data = {
            "_links": {
                "movie": "FALSE LINK"
            },
            "text": "Excellent movie.",
            "timestamp": "00:30:30"
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.CommentList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


    # Test DELETE method
    def test_4_delete(self):
        print("Testing DELETE method for model Comment (expect 204)")

        testObject = Comment.objects.create(text="Excellent movie.", timestamp="00:30:30", movie_id=1, author_id=1)

        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('comment-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Comment.objects.count(), 0)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method without permission
    def test_4_delete_403(self):
        print("Testing DELETE method for model Comment without permission (expect 403)")
        self.client.logout()

        testObject = Comment.objects.create(text="Excellent movie.", timestamp="00:30:30", movie_id=1, author_id=1)

        # Create response
        response = self.client.delete(reverse('comment-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test DELETE method on review that does not exist
    def test_4_delete_404(self):
        print("Testing DELETE method for model Comment that does not exist (expect 404)")
        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('comment-detail', kwargs={'pk': 999}))

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test UPDATE method
    def test_5_update(self):
        print("Testing UPDATE method for model Comment (expect 200)")

        testObject = Comment.objects.create(text="Excellent movie.", timestamp="00:30:30", movie_id=1, author_id=1)

        self.client.login(username='test_admin', password='password')

        data = {
            '_links': {
                'url': self.TESTSERVER_URL + self.url + str(testObject.id),
                'movie': self.movie_url
            },
            'text': "Excellent movie. CHANGED",
            "timestamp": "00:30:11"
        }

        # Create response
        response = self.client.put(reverse('comment-detail', kwargs={'pk': testObject.pk}), data=json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Comment.objects.get().text, 'Excellent movie. CHANGED')
            self.assertEqual(Comment.objects.get().timestamp, '00:30:11')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


class ActorTestCase(APITestCase):
"""
Test case for Actor model
"""
    TESTSERVER_URL = "http://testserver"
    url = reverse('actor-list')

    # Set up factory, create user and movie objects and construct movie url for hyperlinking
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_admin', email='test_admin@…', password='password')

    # Test object creation
    def test_1_object_creation(self):
        print("Testing object creation for object Actor")
        Actor.objects.create(firstname="John", lastname= "Doe", author=self.user)
        testActor = Actor.objects.get(firstname="John")

        try:
            self.assertTrue(isinstance(testActor, Actor))
            self.assertEqual(testActor.firstname, 'John')
            self.assertEqual(testActor.lastname, 'Doe')
            self.assertEqual(str(testActor), testActor.firstname + " " + testActor.lastname) # Test __str__ method
            print("SUCCESS")
        except:
            print("FAILED")

    # Test unique constraint
    def test_1_2_object_unique(self):
        print("Testing unique constraint for object Actor")

        Actor.objects.create(id=1, firstname="John", lastname= "Doe", author=self.user)

        try:
            Actor.objects.create(id=1, firstname="John", lastname= "Doe", author=self.user)
            self.fail("FAILED")
            print("FAILED")
        except exception.IntegrityError:
            print("SUCCESS")
            pass

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Actor (expect 200)")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Actor (expect 201)")
        self.client.login(username='test_admin', password='password')

        data = {
            "firstname": "John",
            "lastname": "Doe"
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ActorList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Actor.objects.count(), 1)
            self.assertEqual(Actor.objects.get().firstname, 'John')
            self.assertEqual(Actor.objects.get().lastname, 'Doe')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test POST method with bad request
    def test_3_post_400(self):
        print("Testing POST method for model Actor with bad request (expect 400)")
        self.client.login(username='test_admin', password='password')

        data = {
            "firstname": ""
        }

        # Create request
        request = self.factory.post(self.url, data, content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ActorList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


    # Test DELETE method
    def test_4_delete(self):
        print("Testing DELETE method for model Actor (expect 204)")

        testObject = Actor.objects.create(id=1, firstname="John", lastname= "Doe", author=self.user)

        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('actor-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Actor.objects.count(), 0)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method without permission
    def test_4_delete_403(self):
        print("Testing DELETE method for model Actor without permission (expect 403)")
        self.client.logout()

        testObject = Actor.objects.create(id=1, firstname="John", lastname= "Doe", author=self.user)

        # Create response
        response = self.client.delete(reverse('actor-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test DELETE method on review that does not exist
    def test_4_delete_404(self):
        print("Testing DELETE method for model Actor that does not exist (expect 404)")
        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('actor-detail', kwargs={'pk': 999}))

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test UPDATE method
    def test_5_update(self):
        print("Testing UPDATE method for model Actor (expect 200)")

        testObject = Actor.objects.create(id=1, firstname="John", lastname= "Doe", author=self.user)

        self.client.login(username='test_admin', password='password')

        data = {
            '_links': {
                'url': self.TESTSERVER_URL + self.url + str(testObject.id),
            },
            "firstname": "Test",
            "lastname": "Testerson"
        }

        # Create response
        response = self.client.put(reverse('actor-detail', kwargs={'pk': testObject.pk}), data=json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Actor.objects.get().firstname, 'Test')
            self.assertEqual(Actor.objects.get().lastname, 'Testerson')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


class CategoryTestCase(APITestCase):
"""
Test case for Category model
"""
    TESTSERVER_URL = "http://testserver"
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
            self.assertTrue(isinstance(testCategory, Category))
            self.assertEqual(testCategory.name, 'TestCategory')
            self.assertEqual(str(testCategory), testCategory.name) # Test __str__ method
            print("SUCCESS")
        except:
            print("FAILED")

    # Test unique constraint
    def test_1_2_object_unique(self):
        print("Testing unique constraint for object Category")

        Category.objects.create(id=1, name="TestCategory")

        try:
            Category.objects.create(id=1, name="TestCategory")
            self.fail("FAILED")
            print("FAILED")
        except exception.IntegrityError:
            print("SUCCESS")
            pass

    # Test GET method
    def test_2_get(self):
        print("Testing GET method for model Category (expect 200)")

        response = self.client.get(self.url, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test POST method
    def test_3_post(self):
        print("Testing POST method for model Category (expect 201)")
        self.client.login(username='test_admin', password='password')

        data = {
            "name": "TestCategory"
        }

        # Create request
        request = self.factory.post(self.url, json.dumps(data), content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.CategoryList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Category.objects.count(), 1)
            self.assertEqual(Category.objects.get().name, 'TestCategory')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test POST method with bad request
    def test_3_post_400(self):
        print("Testing POST method for model Category with bad request (expect 400)")
        self.client.login(username='test_admin', password='password')

        data = {
            "name": "TestCategory"
        }

        # Create request
        request = self.factory.post(self.url, data, content_type='application/hal+json')

        # Add user to request session
        request.user = self.user

        # Get data from view with the user tied to the session
        response = views.ActorList.as_view()(request)

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()


    # Test DELETE method
    def test_4_delete(self):
        print("Testing DELETE method for model Category (expect 204)")

        testObject = Category.objects.create(id=1, name="TestCategory")

        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('category-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Category.objects.count(), 0)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test DELETE method without permission
    def test_4_delete_403(self):
        print("Testing DELETE method for model Category without permission (expect 403)")
        self.client.logout()

        testObject = Category.objects.create(id=1, name="TestCategory")

        # Create response
        response = self.client.delete(reverse('category-detail', kwargs={'pk': testObject.pk}))

        try:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print("SUCCESS")
        except:
            print("FAILED")

    # Test DELETE method on review that does not exist
    def test_4_delete_404(self):
        print("Testing DELETE method for model Category that does not exist (expect 404)")
        self.client.login(username='test_admin', password='password')

        # Create response
        response = self.client.delete(reverse('category-detail', kwargs={'pk': 999}))

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()

    # Test UPDATE method
    def test_5_update(self):
        print("Testing UPDATE method for model Category (expect 200)")

        testObject = Category.objects.create(id=1, name="TestCategory")

        self.client.login(username='test_admin', password='password')

        data = {
            '_links': {
                'url': self.TESTSERVER_URL + self.url + str(testObject.id),
            },
            "name": "TestCategory CHANGED"
        }

        # Create response
        response = self.client.put(reverse('category-detail', kwargs={'pk': testObject.pk}), data=json.dumps(data), content_type='application/hal+json')

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Category.objects.get().name, 'TestCategory CHANGED')
            print("SUCCESS")
        except:
            print("FAILED")

        self.client.logout()
