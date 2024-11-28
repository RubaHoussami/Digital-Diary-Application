from src.crew.base.base_tokenizer import BaseTokenizer

class EmotionTokenizer(BaseTokenizer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmotionTokenizer, cls).__new__(cls)
        return cls._instance

    def tokenize(self, text: str) -> str:
        pass
