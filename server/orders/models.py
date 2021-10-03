from django.db import models
from django.conf import settings


class Order(models.Model):
    class State(models.TextChoices):
        PAID = "PAID"
        UNPAID = "UNPAID"

    date = models.DateField()
    state = models.CharField(max_length=6, choices=State.choices, default=State.UNPAID)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)