import jamspell
import os
import difflib
from src.config import config
from src.logger import logger

"""
to be executed before running:
!wget https://github.com/bakwc/JamSpell-models/raw/master/en.tar.gz
!tar -xvf en.tar.gz

useful:
https://github.com/bakwc/JamSpell?tab=readme-ov-file

might need more training (they recommend training on 1 million new examples) if time permits
"""

class SpellChecker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SpellChecker, cls).__new__(cls)
        return cls._instance

    def __init__(self, language: str = 'en'):
        if not hasattr(self, 'initialized'):
            self.jsp = jamspell.TSpellCorrector()
            model_path = self._get_model_path(language)
            assert os.path.exists(model_path), f"Model path does not exist: {model_path}"
            assert self.jsp.LoadLangModel(model_path), f"Failed to load model from {model_path}"
            self.initialized = True

    def correct(self, text: str) -> str:
        return self.jsp.FixFragment(text)

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

    @staticmethod
    def _get_model_path(language: str) -> str:
        return f"{config.SPELL_CHECKER_MODEL_PATH}/{language}.bin"
