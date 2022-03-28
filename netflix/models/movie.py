from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    imdb = models.FloatField(default=0, max_length=10)
    genre = models.CharField(max_length=30)

    actors = models.ManyToManyField('netflix.Actor')

    def __str__(self):
        return self.name
