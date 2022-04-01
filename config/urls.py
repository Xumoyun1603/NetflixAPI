from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Netflix Application REST API',
        default_version="v1",
        description="Swagger docs for Netflix Application REST API",
        contact=openapi.Contact(
            'Nurimov Xumoyun <tuit20192022@gmail.com>',
        ),
    ),
    public=True,
    permission_classes=(AllowAny, )
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('netflix.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]
