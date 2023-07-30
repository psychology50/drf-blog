from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings

from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='블로그 API',
        default_version="v0.0.1",
        description='API Doc 설명',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="qud1251@gmail.com"),
        license=openapi.License(name="Test License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.user.urls', 'api'))),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')]