FROM python:3.11-slim

WORKDIR /code

# Установка зависимостей
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Копирование кода приложения
COPY ./app /code/app

# Запуск сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
