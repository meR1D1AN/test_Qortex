FROM python:3.13.7-slim

RUN groupadd -g 1000 app_group \
    && useradd -r -u 1000 -g app_group -m -s /sbin/nologin app_user

RUN mkdir -p /app && chown -R app_user:app_group /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install uv

# Копируем только файл с зависимостями
COPY --chown=app_user:app_group pyproject.toml poetry.lock ./

# Генерируем requirements.txt и устанавливаем зависимости с флагом --system
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system -r requirements.txt && \
    pip cache purge && \
    uv cache clean

# Копируем остальной код проекта
COPY --chown=app_user:app_group . .

USER app_user