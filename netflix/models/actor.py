from django.db import models


class Actor(models.Model):

    MALE = 'male'
    FEMALE = 'female'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    name = models.CharField(max_length=200)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)

    def __str__(self):
        return self.name

