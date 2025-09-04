from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogs.views import AlbumViewSet, ArtistViewSet, SongViewSet

router = DefaultRouter()
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"songs", SongViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
