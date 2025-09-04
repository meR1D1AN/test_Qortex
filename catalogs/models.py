import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
)


class Artist(Model):
    name = CharField(
        max_length=55,
        unique=True,
        verbose_name="Имя исполнителя",
        help_text="Введите имя исполнителя",
    )

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.name


class Song(Model):
    title = CharField(
        max_length=125,
        verbose_name="Название песни",
        help_text="Введите название песни",
    )

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

    def __str__(self):
        return self.title


class Album(Model):
    title = CharField(
        max_length=128,
        verbose_name="Название альбома",
        help_text="Введите название альбома",
    )
    release_year = PositiveIntegerField(
        verbose_name="Год выпуска",
        help_text="Введите год выпуска",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year),
        ],
    )
    artist = ForeignKey(
        Artist,
        on_delete=CASCADE,
        related_name="albums",
        verbose_name="Имя исполнителя",
        help_text="Выберите исполнителя",
    )
    songs = ManyToManyField(
        Song,
        through="AlbumSong",
        related_name="albums",
        verbose_name="Песни",
        help_text="Выберите песни",
    )

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        unique_together = (
            "title",
            "artist",
        )

    def __str__(self):
        return f"{self.artist.name} - {self.release_year}"


class AlbumSong(Model):
    album = ForeignKey(
        Album,
        on_delete=CASCADE,
        verbose_name="Альбом",
        help_text="Выберите альбом",
    )
    song = ForeignKey(
        Song,
        on_delete=CASCADE,
        verbose_name="Песня",
        help_text="Выберите песню",
    )
    track_number = PositiveIntegerField(
        validators=[
            MaxValueValidator(2048),
        ]
    )

    class Meta:
        verbose_name = "Альбом и песня"
        verbose_name_plural = "Альбомы и песни"
        unique_together = (
            "album",
            "track_number",
        )

    def __str__(self):
        return f"{self.song.title} (#{self.track_number} в {self.album})"
