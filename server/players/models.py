from django.db import models

from django.db import models
from django.conf import settings

from users.models import User
from games.models import Game

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, related_name='players', on_delete=models.CASCADE)
    #game = models.ForeignKey(Game, related_name='games', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
