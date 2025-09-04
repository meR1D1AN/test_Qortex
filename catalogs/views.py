from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

from catalogs.models import Album, Artist, Song
from catalogs.pagination import CustomLOPagination
from catalogs.serializers import (
    AlbumListRetvieveSerializer,
    AlbumSerializer,
    ArtistListRetrieveSerializer,
    ArtistSerializer,
    SongSerializer,
)
from fixture.fixture import (
    ALBUM_ARTIST,
    ALBUM_ERROR,
    ALBUM_RELEASE_YEAR,
    ALBUM_SETTINGS,
    ALMUB_TITLE,
    ARTIST_200_DESCRIPTION,
    ARTIST_ERROR,
    ARTIST_NAME,
    ARTIST_SETTINGS,
    ID_ARTIST,
    LIMIT,
    OFFSET,
    SONG_200_DESCRIPTION,
    SONG_ERROR,
    SONG_ID,
    SONG_SETTINGS,
    SONG_TITLE,
)


class BaseViewSet(ModelViewSet):
    def get_object(self):
        try:
            return self.model.objects.get(pk=self.kwargs["pk"])
        except self.model.DoesNotExist:
            raise NotFound(self.error_message) from None


@extend_schema(tags=[ARTIST_SETTINGS["name"]])
@extend_schema_view(
    list=extend_schema(
        summary="Список всех исполнителей.",
        description="Получение списка всех исполнителей с пагинацией.\n\n"
        "У каждого исполнителя возвращаются все альбомы с песнями и порядковыми номера в альбоме.",
        parameters=[
            LIMIT,
            OFFSET,
            ARTIST_NAME,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer(many=True),
                description="Успешное получение списка всех исполнителей.",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание нового исполнителя.",
        description="Создание нового исполнителя.\n\nПоле `name` - обязательное.",
        request=ArtistSerializer,
        responses={
            201: OpenApiResponse(
                response=ArtistSerializer,
                description="Успешное создание нового исполнителя.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение информации об исполнителе.",
        description="Получение информации об исполнителе.\n\nНеобходимо передать `id` исполнителя.",
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            ),
        },
    ),
    update=extend_schema(
        summary="Обновление информации об исполнителе.",
        description="Обновление информации об исполнителе.\n\nНеобходимо передать `id` исполнителя.",
        request=ArtistSerializer,
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление информации об исполнителе.",
        description="Частичное обновление информации об исполнителе.\n\nНеобходимо передать `id` исполнителя.",
        request=ArtistSerializer,
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление исполнителя.",
        description="Удаление исполнителя.\n\nНеобходимо передать `id` исполнителя.",
        parameters=[
            ID_ARTIST,
        ],
        responses={
            204: OpenApiResponse(
                description="Успешное удаление исполнителя.",
            )
        },
    ),
)
class ArtistViewSet(BaseViewSet):
    queryset = Artist.objects.all()
    pagination_class = CustomLOPagination
    model = Artist
    error_message = ARTIST_ERROR
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("name",)
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ArtistListRetrieveSerializer
        else:
            return ArtistSerializer


@extend_schema(tags=[SONG_SETTINGS["name"]])
@extend_schema_view(
    list=extend_schema(
        summary="Список всех песен.",
        description="Получение списка всех песен с пагинацией.",
        parameters=[
            LIMIT,
            OFFSET,
            SONG_TITLE,
        ],
        responses={
            200: OpenApiResponse(
                response=SongSerializer(many=True),
                description="Успешное получение списка всех песен.",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание новой песни.",
        description="Создание новой песни.\n\nПоля `title` - обязательные.",
        request=SongSerializer,
        responses={
            201: OpenApiResponse(
                response=SongSerializer,
                description="Успешное создание новой песни.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение информации о песне.",
        description="Получение информации о песне.\n\nНеобходимо передать `id` песни.",
        parameters=[SONG_ID],
        responses={
            200: OpenApiResponse(
                response=SongSerializer,
                description=SONG_200_DESCRIPTION,
            ),
        },
    ),
    update=extend_schema(
        summary="Обновление информации о песне.",
        description="Обновление информации о песне.\n\nНеобходимо передать `id` песни.",
        request=SongSerializer,
        parameters=[
            SONG_ID,
        ],
        responses={
            200: OpenApiResponse(
                response=SongSerializer,
                description=SONG_200_DESCRIPTION,
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление информации о песне.",
        description="Частичное обновление информации о песне.\n\nНеобходимо передать `id` песни.",
        request=SongSerializer,
        parameters=[
            SONG_ID,
        ],
        responses={
            200: OpenApiResponse(
                response=SongSerializer,
                description=SONG_200_DESCRIPTION,
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление песни.",
        description="Удаление песни.\n\nНеобходимо передать `id` песни.",
        parameters=[
            SONG_ID,
        ],
        responses={
            204: OpenApiResponse(
                description="Успешное удаление песни.",
            ),
        },
    ),
)
class SongViewSet(BaseViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = CustomLOPagination
    model = Song
    error_message = SONG_ERROR
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("title",)
    ordering_fields = "__all__"


@extend_schema(tags=[ALBUM_SETTINGS["name"]])
@extend_schema_view(
    list=extend_schema(
        summary="Cписок всех альбомов.",
        description="Получение списка всех альбомов с пагинацией.\n\n"
        "Каждый альбом содержит информацию о его исполнителе и о песнях с порядковыми номерами в альбоме.",
        parameters=[
            LIMIT,
            OFFSET,
            ALMUB_TITLE,
            ALBUM_RELEASE_YEAR,
            ALBUM_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=AlbumListRetvieveSerializer(many=True),
                description="Успешное получение списка всех альбомов.",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание нового альбома.",
        description="Создание нового альбома.\n\n"
        "\tВсе поля обязательные.\n\n `artist` - передаём id исполнителя.\n\n `song` - передаём id песни.",
        request=AlbumSerializer,
        responses={
            201: OpenApiResponse(
                response=AlbumListRetvieveSerializer,
                description="Успешное создание нового альбома.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение информации об альбоме.",
        description="Получение информации об альбоме.\n\nНеобходимо передать `id` альбома.",
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            ),
        },
    ),
    update=extend_schema(
        summary="Обновление информации об альбоме.",
        description="Обновление информации об альбоме.\n\nНеобходимо передать `id` альбома.",
        request=ArtistSerializer,
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление информации об альбоме.",
        description="Частичное обновление информации об альбоме.\n\nНеобходимо передать `id` альбома.",
        request=ArtistSerializer,
        parameters=[
            ID_ARTIST,
        ],
        responses={
            200: OpenApiResponse(
                response=ArtistListRetrieveSerializer,
                description=ARTIST_200_DESCRIPTION,
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление альбома.",
        description="Удаление альбома.\n\nНеобходимо передать `id` альбома.",
        parameters=[
            ID_ARTIST,
        ],
        responses={
            204: OpenApiResponse(
                description="Успешное удаление альбома.",
            )
        },
    ),
)
class AlbumViewSet(BaseViewSet):
    queryset = Album.objects.all()
    pagination_class = CustomLOPagination
    model = Album
    error_message = ALBUM_ERROR
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("title", "release_year", "artist")
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AlbumListRetvieveSerializer
        else:
            return AlbumSerializer
