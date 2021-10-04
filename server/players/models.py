from django.db import models

from django.db import models
from django.conf import settings

from users import User
from games import Game

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = user = models.ForeignKey(Game, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
