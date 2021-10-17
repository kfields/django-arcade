class Message:
    @property
    def typename(self):
        return self.__class__.__name__
    def __str__(self):
        return str(self.__dict__)

class Event(Message):
    def __init__(self, id):
        #TODO:?:GraphQL uses strings for ID's.  This is producing headaches
        self.id = str(id)
