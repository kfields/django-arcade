from django.db import models

from django.db import models
from django.conf import settings

from users.models import User
from games.models import Game

class Player(models.Model):
    user = models.ForeignKey(User, related_name='players', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=1)

    def __str__(self):
        return str(self.id)
