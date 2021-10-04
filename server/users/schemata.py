from schemata import Connection, Edge, Node


class UserNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class UserEdge(Edge):
    def __init__(self, obj, node_class=UserNode):
        super().__init__(obj, node_class)

class UserConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=UserEdge, node_class=UserNode)
