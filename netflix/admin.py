from django.contrib import admin
from .models import Movie, Actor


admin.site.register([Movie, Actor])