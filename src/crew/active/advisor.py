import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel


class Advisor():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Advisor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        model_path = self._get_model_path()
        assert os.path.exists(model_path), f"Model path does not exist: {model_path}"
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.initialized = True
    
    @staticmethod
    def _get_model_path():
        return 'src\models\\advisor_model'

    def advise(self, emotions: list[str], mbti_type: str, events: list[str]) -> str:
        pass