# README
# 🤖 AI Spam Detector API

REST API сервис для автоматической классификации текста как **SPAM** или **NOT SPAM** с использованием машинного обучения (Hugging Face Transformers).

## 📌 Возможности

- ✅ Классификация текста (SPAM / NOT SPAM) через ML-модель
- ✅ Сохранение истории всех запросов в PostgreSQL
- ✅ Просмотр истории с пагинацией
- ✅ Health-check ендпоинт
- ✅ Полная контейнеризация (Docker + Docker Compose)

## 🛠 Технологический стек

- **Backend:** Python 3.11 + FastAPI
- **ML-модель:** Hugging Face Transformers (`mrm8488/bert-tiny-finetuned-sms-spam-detection`)
- **База данных:** PostgreSQL 16
- **Контейнеризация:** Docker + Docker Compose
- **Тестирование API:** Postman

## 🚀 Быстрый старт

### Предварительные требования

- Установленный [Docker](https://docs.docker.com/get-docker/)
- Установленный [Docker Compose](https://docs.docker.com/compose/install/)
- Git (для клонирования)
### Запуск
   ```bash
   git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
   cd ai-spam-detector

#2. Настройка переменных окружения
Создайте файл .env из примера:

bash
cp .env.example .env
Содержимое .env по умолчанию:

env
HUGGINGFACE_MODEL_NAME=mrm8488/bert-tiny-finetuned-sms-spam-detection
POSTGRES_USER=spam_user
POSTGRES_PASSWORD=spam_password
POSTGRES_DB=spam_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
💡 Вы можете изменить модель, указав другую в HUGGINGFACE_MODEL_NAME.
Рекомендуется использовать небольшие модели для запуска без GPU.

#3. Запуск сервиса
bash
docker compose up --build
При первом запуске:

Загрузятся образы Python и PostgreSQL

Установятся зависимости из requirements.txt

Загрузится ML-модель с Hugging Face (~50 МБ)

Создадутся таблицы в базе данных

Первый запуск может занять 2-5 минут. Последующие запуски будут быстрее.

#4. Проверка работоспособности
Откройте в браузере или выполните:

bash
curl http://localhost:8000/health
Ожидаемый ответ:

json
{"status": "ok"}
API доступно по адресу: http://localhost:8000

Автоматическая документация Swagger: http://localhost:8000/docs
 ## API Endpoints
GET / — Информация о сервисе
bash
curl http://localhost:8000/
<details> <summary>Пример ответа</summary>
json
{
  "service": "AI Spam Detector API",
  "version": "1.0.0",
  "endpoints": {
    "POST /analyze": "Analyze text for spam",
    "GET /history": "Get last 20 requests",
    "GET /history/{id}": "Get specific request by ID",
    "GET /health": "Health check"
  }
}
</details>
GET /health — Проверка работоспособности
bash
curl http://localhost:8000/health
Параметр	Значение
Метод	GET
Успешный ответ	200 OK
<details> <summary>Пример ответа</summary>
json
{
  "status": "ok"
}
</details>
POST /analyze — Классификация текста
bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You have won a free iPhone. Click here!"}'
Параметр	Значение
Метод	POST
Content-Type	application/json
Успешный ответ	200 OK
Ошибка валидации	400 Bad Request
Ошибка сервера	500 Internal Server Error
Входные данные:

json
{
  "text": "Текст для проверки на спам"
}
Поле	Тип	Обязательное	Ограничения
text	string	Да	1-2000 символов
Успешный ответ:

json
{
  "result": "SPAM",
  "score": 0.9998
}
Поле	Тип	Описание
result	string	"SPAM" или "NOT SPAM"
score	float	Уверенность модели (0.0 — 1.0)
<details> <summary>Примеры запросов</summary>
SPAM текст:

bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "URGENT! You have won a $1000 gift card. Claim now!"}'
json
{"result": "SPAM", "score": 0.9987}
NOT SPAM текст:

bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Hey, are we still meeting for lunch tomorrow?"}'
json
{"result": "NOT SPAM", "score": 0.9876}
Пустой текст (ошибка):

bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
json
{"detail": "Input text cannot be empty"}
</details>
GET /history — История запросов
bash
curl http://localhost:8000/history
Параметр	Значение
Метод	GET
Успешный ответ	200 OK
Возвращает последние 20 запросов, отсортированных по дате (сначала новые).

<details> <summary>Пример ответа</summary>
json
[
  {
    "id": 5,
    "input_text": "URGENT! Claim your prize now!",
    "result_text": "{\"result\": \"SPAM\", \"score\": 0.9987}",
    "model_name": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
    "created_at": "2026-04-20T15:30:00.123456+00:00"
  },
  {
    "id": 4,
    "input_text": "See you tomorrow at the office",
    "result_text": "{\"result\": \"NOT SPAM\", \"score\": 0.9876}",
    "model_name": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
    "created_at": "2026-04-20T15:25:00.654321+00:00"
  }
]
</details>
GET /history/{id} — Конкретный запрос
bash
curl http://localhost:8000/history/1
Параметр	Значение
Метод	GET
Успешный ответ	200 OK
Не найдено	404 Not Found
<details> <summary>Пример ответа</summary>
json
{
  "id": 1,
  "input_text": "Win a free iPhone now!",
  "result_text": "{\"result\": \"SPAM\", \"score\": 0.9991}",
  "model_name": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
  "created_at": "2026-04-20T10:15:00.000000+00:00"
}
Запись не найдена:

bash
curl http://localhost:8000/history/9999
json
{"detail": "History record with ID 9999 not found."}
</details>
## База данных
Таблица requests_history:

Поле	Тип	Описание
id	SERIAL	Первичный ключ, автоинкремент
input_text	TEXT	Исходный текст запроса
result_text	TEXT	Результат в формате JSON: {"result": "...", "score": ...}
model_name	VARCHAR(255)	Название модели Hugging Face
created_at	TIMESTAMPTZ	Дата и время запроса (автоматически)
## ML Модель
Используется модель: mrm8488/bert-tiny-finetuned-sms-spam-detection

Характеристика	Значение
Архитектура	BERT-tiny
Размер	~17 МБ
Задача	Text Classification (SPAM/HAM)
Язык	Английский
GPU не требуется	
Смена модели: Чтобы использовать другую модель, измените переменную HUGGINGFACE_MODEL_NAME в файле .env и перезапустите контейнеры:

bash
docker compose down
docker compose up --build
Тестирование через Postman
Импорт коллекции
Откройте Postman

Нажмите Import → Upload Files

Выберите файл postman/AI_Spam_Detector.postman_collection.json

Коллекция появится в списке

## Тестовые запросы в коллекции
Запрос	Описание
Health Check	Проверка /health
Analyze - SPAM text	Классификация спам-текста
Analyze - NOT SPAM text	Классификация обычного текста
Analyze - Empty text (ERROR)	Проверка обработки пустого текста
Get History	Получение истории
Get History by ID	Получение записи по ID
Get History - Not Found (ERROR)	Проверка 404 ошибки
## Структура проекта
text
ai-spam-detector/
├── app/                          # Исходный код приложения
│   ├── __init__.py
│   ├── config.py                 # Настройки (загрузка .env)
│   ├── database.py               # Подключение к PostgreSQL + SQLAlchemy
│   ├── main.py                   # Точка входа FastAPI + lifespan + middleware
│   ├── ml_service.py             # Класс SpamDetector (Hugging Face)
│   ├── models.py                 # SQLAlchemy модель RequestHistory
│   ├── schemas.py                # Pydantic схемы (запросы/ответы)
│   └── routes/                   # Роутеры API
│       ├── __init__.py
│       ├── analyze.py            # POST /analyze
│       └── history.py            # GET /history, GET /history/{id}
├── postman/                      # Тестирование API
│   └── AI_Spam_Detector.postman_collection.json
├── .env.example                  # Пример переменных окружения
├── .gitignore                    # Исключения Git
├── docker-compose.yml            # Конфигурация Docker Compose
├── Dockerfile                    # Инструкция сборки Docker-образа
├── README.md                     # Документация проекта
└── requirements.txt              # Python-зависимости
## Конфигурация
Все настройки задаются через переменные окружения в файле .env:

Переменная	Описание	Значение по умолчанию
HUGGINGFACE_MODEL_NAME	Hugging Face модель	mrm8488/bert-tiny-finetuned-sms-spam-detection
POSTGRES_USER	Пользователь PostgreSQL	spam_user
POSTGRES_PASSWORD	Пароль PostgreSQL	spam_password
POSTGRES_DB	Название базы данных	spam_db
POSTGRES_HOST	Хост PostgreSQL	postgres (имя сервиса в Docker)
POSTGRES_PORT	Порт PostgreSQL	5432
## Обработка ошибок
Код	Ситуация	Ответ
400	Пустой текст в запросе	{"detail": "Input text cannot be empty"}
400	Некорректный JSON	{"detail": "..."} (ошибка валидации Pydantic)
404	Запись в истории не найдена	{"detail": "History record with ID X not found."}
500	Ошибка базы данных	{"detail": "Failed to save request history."}
500	Ошибка ML модели	{"detail": "Failed to analyze text. Please try again."}
503	Модель не загружена	{"detail": "ML model is not available..."}
## Логирование
Приложение ведет подробное логирование следующих событий:

## Запуск сервиса

## Загрузка ML модели

## Успешные операции

## Входящие HTTP запросы

## Запросы на анализ текста

## Сохранение в базу данных

## Ошибки подключения к БД

## Ошибки ML модели

## Поиск записей в истории

## Логи выводятся в формате:

text
2026-04-20 15:30:00,123 [INFO] app.routes.analyze: Analyzing text: 'Congratulations!...'
2026-04-20 15:30:00,456 [INFO] app.routes.analyze: Prediction: {'result': 'SPAM', 'score': 0.9998}
2026-04-20 15:30:00,789 [INFO] app.routes.analyze: Saved to history with ID: 42
 Docker команды
bash
# Запуск (с пересборкой)
docker compose up --build

# Запуск в фоне
docker compose up -d --build

# Остановка
docker compose down

# Остановка с удалением томов (сброс БД)
docker compose down -v

# Просмотр логов
docker compose logs -f backend

# Перезапуск
docker compose restart
