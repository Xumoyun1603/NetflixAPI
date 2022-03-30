from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from netflix.models import Movie, Actor, Comment
from netflix.serializers import MovieSerializer, ActorSerializer, CommentSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CommentAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)

        comments = movie.comments.all()

        serializer = CommentSerializer(comments, many=True)

        return Response(data=serializer.data)

    def post(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)

        request.data['user_id'] = request.user.id
        request.data['movie_id'] = movie.id

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            comment = Comment(
                movie_id=data['movie_id'],
                user_id=data['user_id'],
                text=data['text'],
            )
            comment.save()
            movie.comments.add(comment)

            return Response({'status': 'The comment successfully created'})

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None, pk_alt=None):
        movie = get_object_or_404(Movie, pk=pk)
        comment = get_object_or_404(movie.comments, pk=pk_alt)

        serializer = CommentSerializer(comment)

        return Response(data=serializer.data)

    def delete(self, request, pk=None, pk_alt=None):
        movie = get_object_or_404(Movie, pk=pk)
        comment = get_object_or_404(movie.comments, pk=pk_alt)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
