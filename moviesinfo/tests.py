from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from moviesinfo.api import serializers
from moviesinfo import models


class PlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", 
                                             password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 
                                self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")

    # def test_platform_create(self):
    #     data = {
    #         "name": "Netflix",
    #         "about": "#1 Streaming Platform",
    #         "website": "https://netflix.com"
    #     }
    #     response = self.client.post(reverse('platform-list'), data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_platform_list(self):
        response = self.client.get(reverse('platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_platform_ind(self):
        response = self.client.get(reverse('platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MoviesTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")
        self.movies = models.Movies.objects.create(platform=self.stream, title="Example Movie",
                                storyline="Example Movie", active=True)

    def test_movies_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_movies_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_movies_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.movies.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Movies.objects.count(), 1)
        self.assertEqual(models.Movies.objects.get().title, 'Example Movie')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")
        self.movies = models.Movies.objects.create(platform=self.stream, title="Example Movie",
                                storyline="Example Movie", active=True)
        self.movies2 = models.Movies.objects.create(platform=self.stream, title="Example Movie",
                                storyline="Example Movie", active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="Great Movie", 
                                movies=self.movies2, active=True)
    
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "movies": self.movies,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.movies.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(reverse('review-create', args=(self.movies.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "movies": self.movies,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.movies.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great Movie! - Updated",
            "movies": self.movies,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.movies.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/home/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)