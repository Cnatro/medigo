from abc import ABC, abstractmethod


class VectorRepository(ABC):

    @abstractmethod
    def search_symptoms(self, embedding, top_k=5): pass