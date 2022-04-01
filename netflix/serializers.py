from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from netflix.models import Movie, Actor, Comment


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'birthdate', 'gender',)

    def validate(self, data):
        date1 = '1950-01-01'
        date2 = str(data['birthdate'])

        date1 = datetime.strptime(date1, "%Y-%m-%d")
        date2 = datetime.strptime(date2, "%Y-%m-%d")

        if date1 >= date2:
            raise ValidationError(detail='birthdate 01.01.1950 dan katta bo\'lsin')

        return data


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
