FROM python:3.13.3-slim

WORKDIR /app

# Копируем файлы с зависимостями и конфиг
COPY pyproject.toml uv.lock ./
COPY src/configs/settings-example.yaml ./configs/

# Устанавливаем uv (если он не установлен в базовом образе)
RUN pip install --no-cache-dir uv

# Устанавливаем зависимости через uv
RUN uv pip install --system -r pyproject.toml

# Копируем исходный код и остальные файлы
COPY src/ ./src/
COPY src/templates/ ./templates/
COPY src/configs/alembic.ini ./configs/

# Запускаем приложение через granian
CMD ["granian", "--interface", "asgi", "src.app:app"]

