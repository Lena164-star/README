import logging
from transformers import pipeline
from app.config import settings

logger = logging.getLogger(__name__)

# Маппинг меток модели на читаемые названия
LABEL_MAPPING = {
    "LABEL_1": "SPAM",
    "LABEL_0": "NOT SPAM",
    "spam": "SPAM",
    "ham": "NOT SPAM",
    "SPAM": "SPAM",
    "HAM": "NOT SPAM",
}


class SpamDetector:
    """Сервис для классификации текста как SPAM / NOT SPAM."""

    def __init__(self):
        self.model_name = settings.huggingface_model_name
        self.pipeline = None
        self._load_model()

    def _load_model(self) -> None:
        """Загрузка модели с Hugging Face при старте."""
        try:
            logger.info(f"⏳ Loading Hugging Face model: {self.model_name}")
            self.pipeline = pipeline(
                task="text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                truncation=True,
                max_length=512,
            )
            logger.info(f"✅ Model '{self.model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load model '{self.model_name}': {e}")
            raise RuntimeError(f"Cannot load ML model: {e}")

    def predict(self, text: str) -> dict:
        """
        Предсказывает, является ли текст спамом.
        
        Args:
            text: Входной текст для анализа
            
        Returns:
            dict: {"result": "SPAM"|"NOT SPAM", "score": 0.99}
        """
        if not self.pipeline:
            raise RuntimeError("Model pipeline is not initialized")

        try:
            raw_result = self.pipeline(text)[0]
            label = raw_result["label"]
            score = round(raw_result["score"], 4)

            # Преобразуем техническую метку в читаемую
            result_label = LABEL_MAPPING.get(label, label.upper())

            return {
                "result": result_label,
                "score": score
            }
        except Exception as e:
            logger.error(f"Prediction error for text '{text[:100]}...': {e}")
            raise


# Глобальный экземпляр (singleton)
try:
    spam_detector = SpamDetector()
except RuntimeError as e:
    logger.critical(f"Failed to initialize SpamDetector: {e}")
    spam_detector = None
