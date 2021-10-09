from django.db import models

from django.db import models
from django.conf import settings

from players.models import Player

from .state import WaitState, ActiveState, default_state, GameStateEncoder, GameStateDecoder

class Game(models.Model):
    state = models.JSONField(encoder=GameStateEncoder, decoder=GameStateDecoder, default=default_state)

    def __str__(self):
        return str(self.id)

    def join(self, user):
        if Player.objects.filter(user=user, game=self).exists():
            player = Player.objects.get(user=user, game=self)
        #else
        elif len(Player.objects.filter(game=self)) == 0:
            player = Player.objects.create(user=user, game=self, symbol='X')
            self.state = WaitState(self.state.board)
        else:
            player = Player.objects.create(user=user, game=self, symbol='O')
            self.state = ActiveState(self.state.board)
        self.save()
        return player

