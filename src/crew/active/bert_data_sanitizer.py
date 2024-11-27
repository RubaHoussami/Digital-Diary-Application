from src.crew.base.base_data_sanitizer import BaseDataSanitizer
from src.crew.active.spell_checker import SpellChecker
from src.logger import logger


class BERTDataSanitizer(BaseDataSanitizer):
    def __init__(self):
        self.spell_checker = SpellChecker()

    def load(self, path):
        pass

    def sanitize(self, data):
        # preliminary
        data = data.lower()
        data.replace("the", "")
        data.replace("a", "")
        data.replace("an", "")
        data.replace("and", "")
        data.replace("or", "")
        pass

    def validate(self, data):
        pass

    def bertify(self, data):
        pass

    def deep_clean(self, data):
        pass
