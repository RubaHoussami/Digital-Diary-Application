from abc import ABC, abstractmethod


class BaseDataSanitizer(ABC):
    @abstractmethod
    def sanitize(self, data):
        pass

    @abstractmethod
    def deep_clean(self, data):
        pass
