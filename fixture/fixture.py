from drf_spectacular.utils import OpenApiParameter

# Фикстуры для settings
ARTIST_SETTINGS = {
    "name": "Исполнители",
    "description": "Методы для работы с исполнителями.",
}
ALBUM_SETTINGS = {
    "name": "Альбомы",
    "description": "Методы для работы с альбомами.",
}
SONG_SETTINGS = {
    "name": "Песни",
    "description": "Методы для работы с песнями.",
}
# Фикстуры исполнителя
ID_ARTIST = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Исполнителя",
    required=True,
)
ARTIST_ERROR = "Исполнитель с таким id не найден."
ARTIST_200_DESCRIPTION = "Успешное получение информации об исполнителе."
ARTIST_NAME = OpenApiParameter(
    name="name",
    type=str,
    description="Имя исполнителя",
    required=False,
)

# Фикстуры песен
SONG_ID = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Песни",
    required=True,
)
SONG_ERROR = "Песня с таким id не найдена."
SONG_200_DESCRIPTION = "Успешное получение информации о песне."
SONG_TITLE = OpenApiParameter(
    name="title",
    type=str,
    description="Название песни",
    required=False,
)

# Фикстуры альбома
ALBUM_ID = OpenApiParameter(
    name="id",
    type=int,
    location=OpenApiParameter.PATH,
    description="ID Альбома",
    required=True,
)
ALBUM_ERROR = "Альбом с таким id не найден."
ALBUM_200_DESCRIPTION = "Успешное получение информации об альбоме."
ALMUB_TITLE = OpenApiParameter(
    name="title",
    type=str,
    description="Название альбома",
    required=False,
)
ALBUM_RELEASE_YEAR = OpenApiParameter(
    name="release_year",
    type=int,
    description="Год выпуска альбома",
    required=False,
)
ALBUM_ARTIST = OpenApiParameter(
    name="artist",
    type=int,
    description="ID исполнителя",
    required=False,
)

# Фикстуры пагинации
LIMIT = OpenApiParameter(
    name="limit",
    type=int,
    description="Количество записей на одной странице, по умолчанию 10 записей.",
    required=False,
)
OFFSET = OpenApiParameter(
    name="offset",
    type=int,
    description="Начальный индекс для пагинации",
    required=False,
)
