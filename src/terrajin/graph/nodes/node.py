from __future__ import annotations
from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, name: str = None, **kwargs):
        self.name = "" if name is None else str(name)
    
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class InNode(Node):
    def __init__(self, name: str = None, inputs: list[Node] = None, **kwargs):
        self.inputs = [] if inputs is None else list(inputs)
        super().__init__(name = name, **kwargs)

class OutNode(Node):
    def __init__(self, name: str = None, outputs: list[InNode] = None, **kwargs):
        self.outputs = [] if outputs is None else list(outputs)
        self.value = None
        super().__init__(name = name, **kwargs)
        
    def __call__(self, *args, **kwargs):
        return self.value