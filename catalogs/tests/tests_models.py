import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from catalogs.models import Album, AlbumSong, Artist, Song


class TestArtistModel(TestCase):
    def test_create_artist(self):
        artist = Artist.objects.create(name="Тестовый Исполнитель")
        self.assertEqual(artist.name, "Тестовый Исполнитель")
        self.assertEqual(str(artist), "Тестовый Исполнитель")
        self.assertEqual(Artist.objects.count(), 1)

    def test_unique_name(self):
        Artist.objects.create(name="Тестовый Исполнитель")
        with self.assertRaises(IntegrityError):
            Artist.objects.create(name="Тестовый Исполнитель")

    def test_name_max_length(self):
        with self.assertRaises(ValidationError):
            artist = Artist(name="А" * 56)
            artist.full_clean()


class TestSongModel(TestCase):
    def test_create_song(self):
        song = Song.objects.create(title="Тестовая Песня")
        self.assertEqual(song.title, "Тестовая Песня")
        self.assertEqual(str(song), "Тестовая Песня")
        self.assertEqual(Song.objects.count(), 1)

    def test_title_max_length(self):
        with self.assertRaises(ValidationError):
            song = Song(title="А" * 126)
            song.full_clean()


class TestAlbumModel(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Тестовый Исполнитель")

    def test_create_album(self):
        album = Album.objects.create(
            title="Тестовый Альбом",
            release_year=2020,
            artist=self.artist,
        )
        self.assertEqual(album.title, "Тестовый Альбом")
        self.assertEqual(album.release_year, 2020)
        self.assertEqual(album.artist, self.artist)
        self.assertEqual(str(album), "Тестовый Исполнитель - 2020")
        self.assertEqual(Album.objects.count(), 1)

    def test_unique_together_title_artist(self):
        Album.objects.create(title="Тестовый Альбом", release_year=2020, artist=self.artist)
        with self.assertRaises(IntegrityError):
            Album.objects.create(title="Тестовый Альбом", release_year=2021, artist=self.artist)

    def test_release_year_validators(self):
        with self.assertRaises(ValidationError):
            album = Album(title="Тестовый Альбом", release_year=1899, artist=self.artist)
            album.full_clean()

        with self.assertRaises(ValidationError):
            album = Album(
                title="Тестовый Альбом",
                release_year=datetime.date.today().year + 1,
                artist=self.artist,
            )
            album.full_clean()


class TestAlbumSongModel(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Тестовый Исполнитель")
        self.album = Album.objects.create(
            title="Тестовый Альбом",
            release_year=2020,
            artist=self.artist,
        )
        self.song = Song.objects.create(title="Тестовая Песня")

    def test_create_album_song(self):
        album_song = AlbumSong.objects.create(
            album=self.album,
            song=self.song,
            track_number=1,
        )
        self.assertEqual(album_song.album, self.album)
        self.assertEqual(album_song.song, self.song)
        self.assertEqual(album_song.track_number, 1)
        self.assertEqual(str(album_song), "Тестовая Песня (#1 в Тестовый Исполнитель - 2020)")
        self.assertEqual(AlbumSong.objects.count(), 1)

    def test_unique_together_album_track_number(self):
        AlbumSong.objects.create(album=self.album, song=self.song, track_number=1)
        new_song = Song.objects.create(title="Другая Песня")
        with self.assertRaises(IntegrityError):
            AlbumSong.objects.create(album=self.album, song=new_song, track_number=1)

    def test_track_number_validator(self):
        with self.assertRaises(ValidationError):
            album_song = AlbumSong(album=self.album, song=self.song, track_number=2049)
            album_song.full_clean()

    def test_many_to_many_relation(self):
        self.assertEqual(self.album.songs.count(), 1)
        self.assertEqual(self.album.songs.first(), self.song)
        self.assertEqual(self.song.albums.count(), 1)
        self.assertEqual(self.song.albums.first(), self.album)
