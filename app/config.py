import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
HF_MODEL_NAME = os.getenv('HF_MODEL_NAME', 'mrm8488/bert-tiny-finetuned-sms-spam-detection')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
