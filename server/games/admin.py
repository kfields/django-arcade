from django.contrib import admin

from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
