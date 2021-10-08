from schemata import Connection, Edge, Node


class PlayerNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class PlayerEdge(Edge):
    def __init__(self, obj, node_class=PlayerNode):
        super().__init__(obj, node_class)

class PlayerConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PlayerEdge, node_class=PlayerNode)
