from src.crew.base.base_data_sanitizer import BaseDataSanitizer
from src.crew.active.spell_checker import SpellChecker
from src.errors import DangerDetected
from src.logger import logger
import re
from better_profanity import profanity


class DataSanitizer(BaseDataSanitizer):
    def __init__(self):
        self.spell_checker = SpellChecker()

    def sanitize(self, text: str) -> str:
        text = text.lower().strip()
        if self.detect_danger(text):
            raise DangerDetected()

        text = self.spell_checker.correct(text)
        text = self.deep_clean(text)
        text = self.secure(text)

        return text

    def deep_clean(self, text: str) -> str:
        profanity.load_censor_words()
        text = profanity.censor(text, '[CUSSWORD]')
        text = text.replace("[CUSSWORD][CUSSWORD][CUSSWORD][CUSSWORD]", "[CUSSWORD]")
        return text
    
    def secure(self, text: str) -> str:
        text = re.sub(r'\b(?:https?://|www\.)\S+\b', '[MALICIOUS]', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[MALICIOUS]', text)
        return text

    def detect_danger(self, text: str) -> bool:
        words = text.split()

        danger_signals = 0
        for word in words:
            danger_signals += 1 if word in {"hurt", "harm", "end", "kill", "die", "life", "myself", "pain", "suicide", "death", "want", "noose", "rope", "hang", "knife", "cut"} else 0

        return danger_signals >= 2
