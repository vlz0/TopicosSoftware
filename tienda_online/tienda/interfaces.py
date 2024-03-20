from abc import ABC, abstractmethod 

class ImageStorage(ABC):
    @abstractmethod
    def store(self, image): 
        pass 