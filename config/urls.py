from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config import settings

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/catalogs/",
        include("catalogs.urls"),
        name="catalogs",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
