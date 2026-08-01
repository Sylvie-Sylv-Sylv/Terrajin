from abc import ABC, abstractmethod


class Noise(ABC):
    def __init__(self, seed: int):
        self.seed = seed
    
    def randomize_seed(self):
        import random
        self.seed = random.randint(0, 2**31 - 1)

    @abstractmethod
    def __call__(self, *args) -> float:
        pass

class Noise1D(Noise, ABC):
    @abstractmethod
    def __call__(self, x: float) -> float:
        pass

class Noise2D(Noise, ABC):
    @abstractmethod
    def __call__(self, x: float, y: float) -> float:
        pass

class Noise3D(Noise, ABC):
    @abstractmethod
    def __call__(self, x: float, y: float, z: float) -> float:
        pass