# Используем официальный образ Python на основе Alpine
FROM python:3.12.6-alpine

# Установим зависимости системы
RUN apk update \
    && apk add --no-cache build-base mysql-dev linux-headers libffi-dev

# Устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем исходный код проекта в рабочую директорию
COPY . /app

# Устанавливаем переменные окружения для базы данных (без значений)
ENV MYSQL_HOST \
    MYSQL_DATABASE \
    MYSQL_USER \
    MYSQL_PASSWORD

# Команда для запуска приложения
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
