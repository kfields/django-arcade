class Schemata:
    def __init__(self):
        self.typename = self.__class__.__name__
    def wire(self):
        return {}

class Connection(Schemata): 
    def __init__(self, objs, edge_class, node_class):
        super().__init__()
        self.edges = []
        self.pageInfo = None
        for obj in objs:
            self.edges.append(edge_class(obj, node_class))

    def wire(self):
        result = {
            '__typename': self.typename,
            'edges': [edge.wire() for edge in self.edges],
            'pageInfo': self.pageInfo
            }
        return result

class Edge(Schemata):
    def __init__(self, obj, node_class):
        super().__init__()
        self.cursor = ""
        self.node = node_class(obj)

    def wire(self):
        result = {
            '__typename': self.typename,
            'cursor': self.cursor,
            'node': self.node.wire()
        }
        return result

class Node(Schemata):
    def __init__(self, objekt):
        super().__init__()
        self.objekt = objekt

    def wire(self):
        # result = self.objekt.__dict__
        result = vars(self.objekt)
        result['__typename'] = self.typename,
        return result
