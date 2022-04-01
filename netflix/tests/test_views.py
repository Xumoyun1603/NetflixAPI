from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.test import TestCase
from netflix.models import Actor, Movie
from django.contrib.auth import get_user_model

User = get_user_model()


class TestMovieViewSet(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            'john', 'john01@gmail.com', 'john12345$'
        )
        self.token = Token.objects.create(user=self.user)
        self.actor = Actor.objects.create(
            name='Tom Cruise', birthdate='1962-07-03', gender='male'
        )
        self.movie1 = Movie.objects.create(
            name='Mission Impossible', year='1996-05-02', imdb=9.5, genre='Adventure',
        )
        self.movie2 = Movie.objects.create(
            name='The Pursuit of Happiness', year='2006-12-15', imdb=7.9, genre='Drama',
        )
        self.movie1.actors.add(self.actor)
        self.movie2.actors.add(self.actor)

        self.client = APIClient()

    def test_get_all_movies(self):
        token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        response = self.client.get('/movies/', token)
        data = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 2)
        self.assertIsNotNone(data[0]['id'])
        self.assertEquals(data[0]['name'], 'Mission Impossible')
        self.assertEquals(data[0]['year'], '1996-05-02')
        self.assertEquals(data[0]['imdb'], 9.5)
        self.assertEquals(data[0]['genre'], 'Adventure')

    def test_search_movies(self):
        token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        response = self.client.get('/movies/?search=Mission Impossible', token)
        data = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['name'], 'Mission Impossible')

    def test_ordering_imdb(self):
        token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        response = self.client.get('/movies/?ordering=-imdb', token)
        data = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 2)
        self.assertEquals(data[0]['name'], 'Mission Impossible')
        self.assertEquals(data[1]['name'], 'The Pursuit of Happiness')