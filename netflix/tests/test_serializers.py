from django.test import TestCase
from netflix.models import Movie, Actor, Comment
from netflix.serializers import MovieSerializer, ActorSerializer, CommentSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class TestActorSerializer(TestCase):
    def setUp(self) -> None:
        self.actor = Actor.objects.create(
            name='John', birthdate='1949-05-29', gender='male'
        )

    def test_actor_fields_contents(self):
        data = ActorSerializer(self.actor).data

        self.assertIsNotNone(data['id'])
        self.assertEquals(data['name'], 'John')
        self.assertEquals(data['birthdate'], '1949-05-29')
        self.assertEquals(data['gender'], 'male')

    def test_validate_source(self):
        data = {
            "name": 'John',
            "birthdate": '1950-01-01',
            "gender": 'male'
        }
        serializer = ActorSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class TestMovieSerializer(TestCase):
    def setUp(self) -> None:
        self.actor = Actor.objects.create(
            name='Tom Cruise', birthdate='1962-07-03', gender='male'
        )
        self.movie = Movie.objects.create(
            name='Mission Impossible', year='1996-05-02', imdb=9.5, genre='Adventure',
        )
        self.movie.actors.add(self.actor)

    def test_movie_fields_contents(self):
        data = MovieSerializer(self.movie).data

        self.assertIsNotNone(data['id'])
        self.assertEquals(data['name'], 'Mission Impossible')
        self.assertEquals(data['year'], '1996-05-02')
        self.assertEquals(data['imdb'], 9.5)


class TestCommentSerializer(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            'john', 'john01@gmail.com', 'john12345$'
        )
        self.actor = Actor.objects.create(
            name='Tom Cruise', birthdate='1962-07-03', gender='male'
        )
        self.movie = Movie.objects.create(
            name='Mission Impossible', year='1996-05-02', imdb=9.5, genre='Adventure',
        )
        self.movie.actors.add(self.actor)

        self.comment = Comment.objects.create(
            movie_id=self.movie, user_id=self.user, text='Test comment'
        )

    def test_comment_fields_contents(self):
        data = CommentSerializer(self.comment).data

        self.assertIsNotNone(data['id'])
        self.assertEquals(data['text'], 'Test comment')
        self.assertEquals(data['created_date'], '2022-04-01')
        self.assertEquals(data['movie_id'], 1)
        self.assertEquals(data['user_id'], 1)

