import os
import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker

from catalogs.models import Album, AlbumSong, Artist, Song


class Command(BaseCommand):
    """
    Команда для добавления данных и создание админа.
    """

    def handle(self, *args, **options):
        self.fake = Faker("ru_RU")  # Русская локализация
        self.max_attempts = 10  # Максимальное количество попыток для уникальности
        with transaction.atomic():
            self.create_admin()
            artists = self.add_artist(10)
            songs = self.add_song(100)
            self.add_album(23, artists, songs)

    def add_artist(self, count):
        artists = []
        for _ in range(count):
            attempts = 0
            while attempts < self.max_attempts:
                name = self.fake.name()
                if not Artist.objects.filter(name=name).exists():
                    artists.append(Artist(name=name))
                    break
                attempts += 1
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Не удалось сгенерировать уникальное имя для исполнителя после {self.max_attempts} попыток"
                    )
                )
        if artists:
            Artist.objects.bulk_create(artists, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(artists)} исполнителей."))
        return list(Artist.objects.order_by("-id")[: len(artists)])

    def add_song(self, count):
        songs = [
            Song(
                title=self.fake.sentence(nb_words=3, variable_nb_words=True),
            )
            for _ in range(count)
        ]
        Song.objects.bulk_create(songs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(songs)} песен."))
        return list(Song.objects.order_by("-id")[: len(songs)])

    def add_album(self, count, artists, songs):
        albums = []
        album_songs = []

        for _ in range(count):
            artist = random.choice(artists)
            attempts = 0
            while attempts < self.max_attempts:
                try:
                    title = self.fake.sentence(
                        nb_words=2,
                        variable_nb_words=True,
                    )
                    if not Album.objects.filter(title=title, artist=artist).exists():
                        album = Album.objects.create(
                            title=title,
                            release_year=random.randint(1970, 2025),
                            artist=artist,
                        )
                        albums.append(album)
                        selected_songs = random.sample(
                            songs,
                            min(random.randint(3, 7), len(songs)),
                        )
                        for index, song in enumerate(selected_songs, start=1):
                            album_songs.append(AlbumSong(album=album, song=song, track_number=index))
                        break
                except self.fake.unique.UniqueException:
                    attempts += 1
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Не удалось сгенерировать уникальное название альбома "
                        f"для {artist.name} после {self.max_attempts} попыток"
                    )
                )
        if albums:
            Album.objects.bulk_create(albums, ignore_conflicts=True)
        if album_songs:
            AlbumSong.objects.bulk_create(album_songs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Добавлено {len(album_songs)} связей альбом-песня."))
        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(albums)} альбомов."))
        return albums

    def create_admin(self):
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")
        if not username or not password:
            self.stdout.write(self.style.ERROR("ADMIN_USERNAME и ADMIN_PASSWORD должны быть заданы в .env"))
            return
        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(
                username=username,
                first_name="Admin",
                last_name="Admin",
            )
            admin.set_password(password)
            admin.save()
            self.stdout.write(self.style.SUCCESS(f"Админ {username} создан."))
        else:
            self.stdout.write(self.style.WARNING(f"Админ {username} уже существует!!!"))
