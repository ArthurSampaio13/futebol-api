from abc import ABC, abstractmethod

class FootballDataService(ABC):
    @abstractmethod
    def get_data(self):
        pass