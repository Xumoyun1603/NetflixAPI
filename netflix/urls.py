from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    MovieViewSet, ActorViewSet, CommentAPIView, CommentDetailAPIView
)


router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', ActorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token),
    path('movies/<int:pk>/comments/', CommentAPIView.as_view(), name='comments'),
    path('movies/<int:pk>/comments/<int:pk_alt>/', CommentDetailAPIView.as_view(), name='comment'),
]