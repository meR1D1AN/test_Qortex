import datetime

from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from catalogs.models import Album, AlbumSong, Artist, Song


class ArtistSerializer(ModelSerializer):
    """
    Сериализатор Исполнителя для action CREATE, UPDATE, PARTIAL_UPDATE, DESTROY.
    """

    class Meta:
        model = Artist
        fields = (
            "id",
            "name",
        )


class SongSerializer(ModelSerializer):
    """
    Сериализатор песени всех action.
    """

    class Meta:
        model = Song
        fields = (
            "id",
            "title",
        )


class AlbumSongSerializer(ModelSerializer):
    """
    Промежуточный сериализатор альбома для action CREATE, UPDATE, PARTIAL_UPDATE, DESTROY.
    """

    class Meta:
        model = AlbumSong
        fields = (
            "song",
            "track_number",
        )

    def validate(self, data):
        # Проверяем уникальность track_number для альбома
        album = self.context.get("album")
        track_number = data.get("track_number")
        if (
            album
            and AlbumSong.objects.filter(
                album=album,
                track_number=track_number,
            ).exists()
        ):
            raise ValidationError({"track_number": f"Трек с номером {track_number} уже существует в этом альбоме."})
        return data


class AlbumSongListRetrieveSerializer(ModelSerializer):
    """
    Промежуточный сериализатор альбома для action LIST и RETRIEVE.
    """

    song = SongSerializer()

    class Meta:
        model = AlbumSong
        fields = (
            "song",
            "track_number",
        )


class AlbumSerializer(ModelSerializer):
    """
    Сериализатор альбома для action CREATE, UPDATE, PARTIAL_UPDATE, DESTROY.
    """

    songs = AlbumSongSerializer(many=True, write_only=True)

    class Meta:
        model = Album
        fields = (
            "id",
            "title",
            "release_year",
            "artist",
            "songs",
        )

    def validate(self, data):
        release_year = data.get("release_year")
        songs_data = data.get("songs", [])
        track_numbers = [s["track_number"] for s in songs_data]
        if release_year:
            if release_year < 1900:
                raise ValidationError({"release_year": "Год выпуска альбома не может быть меньше 1900."})
            if release_year > datetime.date.today().year:
                raise ValidationError({"release_year": "Год выпуска альбома не может быть больше текущего года."})
        if len(track_numbers) != len(set(track_numbers)):
            raise ValidationError({"songs": "Трек с таким номером уже есть в альбоме."})
        return data

    def create(self, validated_data):
        songs_data = validated_data.pop("songs")
        album = Album.objects.create(**validated_data)
        for song_data in songs_data:
            AlbumSong.objects.create(album=album, **song_data)
        return album

    def update(self, instance, validated_data):
        songs_data = validated_data.pop("songs", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if songs_data is not None:
            instance.albumsong_set.all().delete()
            for song_data in songs_data:
                AlbumSong.objects.create(album=instance, **song_data)
        return instance


class AlbumListRetvieveSerializer(AlbumSerializer):
    """
    Сериализатор альбома для action LIST и RETRIEVE.
    """

    artist = ArtistSerializer()
    songs = AlbumSongListRetrieveSerializer(source="albumsong_set", many=True)

    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields


class ArtistListRetrieveSerializer(ArtistSerializer):
    """
    Сериализатор Исполнителя для action LIST и RETRIEVE.
    """

    albums = AlbumListRetvieveSerializer(many=True, read_only=True)

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ("albums",)
