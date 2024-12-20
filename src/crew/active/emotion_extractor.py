import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.crew.base.base_extractor import BaseExtractor


class EmotionExtractor(BaseExtractor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmotionExtractor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            model_path = self._get_model_path()
            assert os.path.exists(model_path), f"Model path does not exist: {model_path}"
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.initialized = True

    @staticmethod
    def _get_model_path():
        return 'src\models\emotion_extractor'

    def tokenize(self, text: str) -> dict:
        return self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

    def extract(self, text: str) -> str:
        tokenized_text = self.tokenize(text)

        with torch.no_grad():
            outputs = self.model(**tokenized_text)
            logits = outputs.logits

        predicted_class_id = torch.argmax(logits, dim=1).tolist()
        label = self.model.config.id2label[predicted_class_id[0]]
        emotions = ["joy", "anger", "love", "sadness", "fear", "surprise"]
        emotion = emotions[int(label.split("_")[1])]

        return emotion
