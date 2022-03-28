from django.urls import path
from .views import MoviesAPIView, ActorsAPIView


urlpatterns = [
    path('movies/', MoviesAPIView.as_view(), name='movies'),
    path('actors/', ActorsAPIView.as_view(), name='actors'),
]