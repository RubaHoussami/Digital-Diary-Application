from abc import ABC, abstractmethod

class BaseExtractor(ABC): 
    @abstractmethod
    def tokenize(self, text: str) -> dict:
        pass

    @abstractmethod
    def extract(self, text: str) -> str:
        pass
