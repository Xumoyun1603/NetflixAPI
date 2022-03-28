from rest_framework.views import APIView
from rest_framework.response import Response

from netflix.models import Movie, Actor
from netflix.serializers import MovieSerializer, ActorSerializer


class MoviesAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(data=serializer.data)


class ActorsAPIView(APIView):
    def get(self, request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        return Response(data=serializer.data)

