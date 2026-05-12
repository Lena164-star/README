import logging
from transformers import pipeline
from .config import settings

logger = logging.getLogger(__name__)

class SpamDetector:
    def __init__(self):
        self.model_name = settings.huggingface_model_name
        self.pipeline = None
        self.load_model()

    def load_model(self):
        """Загружает модель машинного обучения из Hugging Face."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            # Создаем pipeline для классификации текста
            self.pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name
            )
            logger.info(f"Model '{self.model_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model '{self.model_name}': {e}")
            raise RuntimeError(f"Could not load model: {e}")

    def predict(self, text: str) -> dict:
        """Делает предсказание (спам или нет)."""
        if not self.pipeline:
            raise RuntimeError("Prediction model is not loaded.")
        
        result = self.pipeline(text)[0]
        return {
            "result": result['label'],
            "score": result['score']
        }

spam_detector = SpamDetector()
