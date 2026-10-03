from abc import ABC, abstractmethod

class DecisionModel(ABC):

    @abstractmethod
    def choice(self, sample):
        pass

    @abstractmethod
    def noul(self, sample):
        pass

    @abstractmethod
    def score(self, sample):
        pass