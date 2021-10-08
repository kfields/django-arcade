class Message:
    @property
    def typename(self):
        return self.__class__.__name__

class Event(Message):
    def __init__(self, id):
        self.id = id
