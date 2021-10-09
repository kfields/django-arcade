from django.db import models

from django.db import models
from django.conf import settings

#from users.models import User
#from games.models import Game

class Player(models.Model):
    user = models.ForeignKey('users.User', related_name='user_players', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', related_name='game_players', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=1)

    def __str__(self):
        return str(self.id)
