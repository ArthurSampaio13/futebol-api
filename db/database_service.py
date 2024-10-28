from abc import ABC, abstractmethod

class DatabaseService(ABC):
    @abstractmethod
    def insert_data(self, query, data):
        pass