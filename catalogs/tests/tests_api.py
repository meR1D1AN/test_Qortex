from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from catalogs.models import Album, AlbumSong, Artist, Song


class TestArtistAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artist.objects.create(name="Тестовый Исполнитель")

    def test_list_artists(self):
        response = self.client.get(reverse("artist-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Тестовый Исполнитель")
        self.assertIn("albums", response.data["results"][0])

    def test_retrieve_artist(self):
        response = self.client.get(reverse("artist-detail", args=[self.artist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый Исполнитель")
        self.assertEqual(response.data["id"], self.artist.id)

    def test_create_artist(self):
        data = {"name": "Новый Исполнитель"}
        response = self.client.post(reverse("artist-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 2)
        self.assertTrue(Artist.objects.filter(name="Новый Исполнитель").exists())

    def test_create_duplicate_artist(self):
        data = {"name": "Тестовый Исполнитель"}
        response = self.client.post(reverse("artist-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_artist(self):
        data = {"name": "Обновлённый Исполнитель"}
        response = self.client.put(reverse("artist-detail", args=[self.artist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, "Обновлённый Исполнитель")


class TestSongAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.song = Song.objects.create(title="Тестовая Песня")

    def test_list_songs(self):
        response = self.client.get(reverse("song-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Тестовая Песня")

    def test_create_song(self):
        data = {"title": "Новая Песня"}
        response = self.client.post(reverse("song-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 2)
        self.assertTrue(Song.objects.filter(title="Новая Песня").exists())

    def test_update_song(self):
        data = {"title": "Обновлённая Песня"}
        response = self.client.put(reverse("song-detail", args=[self.song.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, "Обновлённая Песня")


class TestAlbumAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artist.objects.create(name="Тестовый Исполнитель")
        self.song1 = Song.objects.create(title="Песня 1")
        self.song2 = Song.objects.create(title="Песня 2")
        self.album = Album.objects.create(
            title="Тестовый Альбом",
            release_year=2020,
            artist=self.artist,
        )
        AlbumSong.objects.create(album=self.album, song=self.song1, track_number=1)
        AlbumSong.objects.create(album=self.album, song=self.song2, track_number=2)

    def test_list_albums(self):
        response = self.client.get(reverse("album-list"))
        response_results = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_results), 1)
        self.assertEqual(response_results[0]["title"], "Тестовый Альбом")
        self.assertEqual(response_results[0]["artist"]["name"], "Тестовый Исполнитель")
        self.assertEqual(len(response_results[0]["songs"]), 2)
        self.assertEqual(response_results[0]["songs"][0]["song"]["title"], "Песня 1")
        self.assertEqual(response_results[0]["songs"][0]["track_number"], 1)

    def test_retrieve_album(self):
        response = self.client.get(reverse("album-detail", args=[self.album.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Тестовый Альбом")
        self.assertEqual(len(response.data["songs"]), 2)

    def test_create_album(self):
        data = {
            "title": "Новый Альбом",
            "release_year": 2021,
            "artist": self.artist.id,
            "songs": [
                {"song": self.song1.id, "track_number": 1},
                {"song": self.song2.id, "track_number": 2},
            ],
        }
        response = self.client.post(reverse("album-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
        album = Album.objects.get(title="Новый Альбом")
        self.assertEqual(album.songs.count(), 2)
        self.assertTrue(AlbumSong.objects.filter(album=album, track_number=1).exists())

    def test_create_duplicate_track_number(self):
        data = {
            "title": "Новый Альбом",
            "release_year": 2021,
            "artist": self.artist.id,
            "songs": [
                {"song": self.song1.id, "track_number": 1},
                {"song": self.song2.id, "track_number": 1},  # Дублирующий track_number
            ],
        }
        response = self.client.post(reverse("album-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_album(self):
        data = {
            "title": "Обновлённый Альбом",
            "release_year": 2022,
            "artist": self.artist.id,
            "songs": [
                {"song": self.song1.id, "track_number": 1},
            ],
        }
        response = self.client.put(reverse("album-detail", args=[self.album.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, "Обновлённый Альбом")
        self.assertEqual(self.album.release_year, 2022)
        self.assertEqual(self.album.songs.count(), 1)
        self.assertTrue(AlbumSong.objects.filter(album=self.album, track_number=1).exists())

    def test_invalid_release_year(self):
        data = {
            "title": "Новый Альбом",
            "release_year": 1899,  # Нарушение MinValueValidator
            "artist": self.artist.id,
            "songs": [{"song": self.song1.id, "track_number": 1}],
        }
        response = self.client.post(reverse("album-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
