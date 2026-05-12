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

1. **Клонируйте репозиторий:**
   ```bash
   git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
   cd ai-spam-detector
