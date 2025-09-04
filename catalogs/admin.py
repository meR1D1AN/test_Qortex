from django.contrib import admin
from django.contrib.admin import ModelAdmin

from catalogs.models import Album, Artist, Song


@admin.register(Artist)
class ArtistAdmin(ModelAdmin):
    """
    Административная панель для модели Исполнитель.
    """

    list_display = (
        "id",
        "name",
    )


@admin.register(Song)
class SongAdmin(ModelAdmin):
    """
    Административная панель для модели Песня.
    """

    list_display = (
        "id",
        "title",
    )


@admin.register(Album)
class AlbumAdmin(ModelAdmin):
    """
    Административная панель для модели Альбом.
    """

    list_display = (
        "id",
        "title",
        "artist",
        "release_year",
    )
