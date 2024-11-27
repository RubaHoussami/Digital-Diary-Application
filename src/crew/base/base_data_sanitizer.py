from abc import ABC, abstractmethod


class BaseDataSanitizer(ABC):
    @abstractmethod
    def load(self, path): # might create a loader class
        pass

    @abstractmethod
    def sanitize(self, data):
        pass

    @abstractmethod
    def tokenize(self, data):
        pass

    @abstractmethod
    def validate(self, data):
        pass
