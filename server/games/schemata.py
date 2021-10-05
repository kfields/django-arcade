from schemata import Connection, Edge, Node


class GameNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class GameEdge(Edge):
    def __init__(self, obj, node_class=GameNode):
        super().__init__(obj, node_class)

class GameConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=GameEdge, node_class=GameNode)
