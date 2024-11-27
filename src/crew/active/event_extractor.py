from src.crew.base.base_extractor import BaseExtractor

class EventExtractor(BaseExtractor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventExtractor, cls).__new__(cls)
        return cls._instance

    def extract(self, text: str) -> str:
        pass
