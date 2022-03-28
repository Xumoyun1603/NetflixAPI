from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from netflix.models import Movie, Actor
from netflix.serializers import MovieSerializer, ActorSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def add_actor(self, request, *args, **kwargs):
        movie = self.get_object()

        serializer = ActorSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            actor, created = Actor.objects.get_or_create(
                name=data['name'],
                birthdate=data['birthdate'],
                gender=data['gender']
            )
            movie.actors.add(actor)
            movie.save()

            return Response({'status': "The actor successfully joined"})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def remove_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data['actor_id']

        for actor in movie.actors.all():
            if actor.id == int(actor_id):
                movie.actors.remove(actor.id)

        return Response({'status': 'The actor was successfully removed'})

    @action(detail=True, methods=['GET'])
    def actors(self, request, *args, **kwargs):
        movie = self.get_object()
        actors = movie.actors.all()

        serializer = ActorSerializer(actors, many=True)

        return Response(data=serializer.data)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

