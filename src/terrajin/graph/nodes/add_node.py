from terrajin.graph.nodes.node import InNode, Node


class AddNode(InNode):
    def __init__(self, name: str = None, inputs: list[Node] = None, **kwargs):
        super().__init__(name, inputs, **kwargs)
        
    def __call__(self, *args, **kwargs):
        return sum([inp() for inp in self.inputs])