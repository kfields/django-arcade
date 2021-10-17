from django.db import models

from django.db import models
from django.conf import settings

#from users.models import User
#from games.models import Game

def get_prev_player():
    pass

def get_next_player():
    pass

class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    prev = models.OneToOneField('self', blank=True, null=True, related_name='next', on_delete=models.SET(get_prev_player))
    #next = models.OneToOneField('players.Player', related_name='prev', on_delete=models.SET(get_next_player))
    #user = models.ForeignKey('users.User', related_name='user_players', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    #game = models.ForeignKey('games.Game', related_name='game_players', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=1)

    def __str__(self):
        return str(self.id)
