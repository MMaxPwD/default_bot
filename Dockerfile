# Выбираем образ, от которого наследуемся.(сверяем чтоб версии питона совпадали)
FROM python:3.12-slim
LABEL authors="maxim"


# RUN — всегда новые слой, выполняем обновления системы вобразе
RUN apt-get update && apt-get upgrade -y

# WORKDIR — указывает рабочую директорию внутри контейнера. Если директория не существует, она будет создана автоматически.
WORKDIR /app

# COPY — копируем в формате COPY <src>(папка где находится докерфайл) <dest>(созданная папка в данном случае app)
COPY . /app


RUN pip install --upgrade pip && \
    pip install poetry==1.8.1 && \
    pip install requests==2.31.0

# Настройка Poetry для использования глобального окружения Python. Не создаем вирутальное окружение.
RUN poetry config virtualenvs.create false

# Установка зависимостей проекта
RUN poetry install --no-interaction --no-ansi --no-dev --no-root


#Устаналиваем source на папку
ENV PYTHONPATH=/app/src

#Что нужно запустить, например alembic. если через compose то алембик прописываем там
#CMD ["python", "src/main.py"]
CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]
