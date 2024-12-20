from textblob import TextBlob
import difflib

class SpellChecker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SpellChecker, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def correct(self, text: str) -> str:
        blob = TextBlob(text)
        return str(blob.correct())

    @staticmethod
    def compute_mistake_ratio(original_text: str, corrected_text: str) -> float:
        original_words = original_text.split()
        corrected_words = corrected_text.split()

        matcher = difflib.SequenceMatcher(None, original_words, corrected_words)
        differences = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ('replace', 'delete', 'insert'):
                differences += max(i2 - i1, j2 - j1)

        return differences / len(original_words) if original_words else 0.0
