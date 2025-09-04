# API музыкального каталога
Это проект Django, который предоставляет API для управления каталогом исполнителей, их альбомов и песен.
## Запуск проекта
1. Убедитесь, что у вас установлен Docker.
2. Клонируйте репозиторий и перейдите в директорию проекта:
```bash
git clone https://github.com/meR1D1AN/test_Qortex.git
cd test_Qortex
```
3. Скопируйте файл, и внесите недостающие данные:
```bash
cp .env.sample .env
```
4. Запуск проекта с помощью Docker:

```bash
docker compose up -d --build
```
5. Документация [ссылка](https://localhost/api/v1/docs)
---
## Какой стек использовался:

- Python - 3.13
- DRF - 3.16.1
- Psycopg2-binary - 2.9.10
- Gunicorn - 23.0
- DRF-spectacular - 0.28
- Django-filter - 25.1 (добавил от себя)
- Faker - 37.6 (добавил от себя)
---

### При запуске проекта, в нём с помощью команды `python3 manage.py test_data` - уже будут заполнены данные.

Провести тестирование:
```bash
docker exec -it api_qortex coverage run manage.py test && docker exec -it api_qortex coverage report
```