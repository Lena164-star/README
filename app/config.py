from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Spam Detector"
    huggingface_model_name: str = "mrm8488/bert-tiny-finetuned-sms-spam-detection"

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int = 5432

    class Config:
        env_file = ".env" # Путь к файлу с переменными окружения

settings = Settings()
