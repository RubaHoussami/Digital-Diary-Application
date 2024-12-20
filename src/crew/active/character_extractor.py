import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.crew.base.base_extractor import BaseExtractor


class CharacterExtractor(BaseExtractor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CharacterExtractor, cls).__new__(cls)
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
        return 'src\models\character_extractor'

    def tokenize(self, text: str) -> dict:
        return self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

    def extract(self, text: str) -> tuple[dict[str, int], str]:
        tokenized_text = self.tokenize(text)

        with torch.no_grad():
            outputs = self.model(**tokenized_text)
            logits = outputs.logits

        logits = logits.squeeze().tolist()

        trait_names = ["agreeableness", "openness", "conscientiousness", "extraversion", "neuroticism"]
        ocean5_scores = {trait_names[i]: min(max(int(logits[i]), 0), 100) for i in range(len(trait_names))}

        return ocean5_scores

    def get_mbti_type(self, ocean5_scores: dict[str, float]) -> str:
        openness = ocean5_scores["openness"]
        conscientiousness = ocean5_scores["conscientiousness"]
        extraversion = ocean5_scores["extraversion"]
        agreeableness = ocean5_scores["agreeableness"]
        neuroticism = ocean5_scores["neuroticism"]

        if neuroticism > 50:
            ei = "I" if extraversion < 60 else "E"
        else:
            ei = "E" if extraversion > 40 else "I"

        sn = "N" if openness > 50 else "S"

        if neuroticism > 50:
            tf = "F" if agreeableness > 40 else "T"
        else:
            tf = "T" if agreeableness < 60 else "F"

        if neuroticism > 50:
            jp = "J" if conscientiousness > 40 else "P"
        else:
            jp = "P" if conscientiousness < 60 else "J"

        mbti_type = ei + sn + tf + jp
        return mbti_type