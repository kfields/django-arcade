import uuid
from django.db import models

from django.db import models
from django.conf import settings

from players.models import Player

from .state import default_state, GameStateEncoder, GameStateDecoder

class Game(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.JSONField(encoder=GameStateEncoder, decoder=GameStateDecoder, default=default_state)

    def __str__(self):
        return str(self.id)

    def enter(self, state):
        if self.state:
            self.state.exit()
        self.state = state
        state.enter()

    def join(self, user):
        return self.state.join(self, user)

    def mark(self, user, x, y):
        return self.state.mark(self, user, x, y)