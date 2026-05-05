import logging
from transformers import pipeline
from .config import HF_MODEL_NAME

logger = logging.getLogger(__name__)

class SpamClassifier:
    def __init__(self):
        self.model_name = HF_MODEL_NAME
        logger.info(f"Loading Hugging Face model: {self.model_name}")
        try:
            self.pipeline = pipeline("text-classification", model=self.model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Model loading error: {e}")

    def predict(self, text: str):
        result = self.pipeline(text[:512])  # ограничим длину (модели BERT обычно 512 токенов)
        # result = [{'label': 'LABEL_1', 'score': 0.99}, ...]
        label = result[0]['label']
        score = result[0]['score']
        # Приведём к читаемому виду: LABEL_1 -> spam, LABEL_0 -> ham
        spam_label = "spam" if label == "LABEL_1" else "ham"
        return spam_label, score

# Синглтон
classifier = SpamClassifier()
