from django.db import models

from django.db import models
from django.conf import settings

class Game(models.Model):
    state = models.CharField(max_length=9)
    block = models.TextField(blank=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return self.title
