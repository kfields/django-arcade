from loguru import logger

from channels.db import database_sync_to_async

from .hub import hub, GameSubscriber, GameEvent

from schema.base import mutation
from users.jwt import load_user
from .models import Game


@mutation.field("createGame")
@database_sync_to_async
def resolve_create_game(_, info):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("You can't do that!")

    game = Game.objects.create(state=" " * 9)

    return game


@mutation.field("updateGame")
@database_sync_to_async
def resolve_update_game(_, info, id, data):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("You can't do that!")

    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        logger.debug("Game not found")
        raise Exception("Game not found")

    title = data.get("title", None)
    block = data.get("block", None)
    body = data.get("body", None)

    game.title = title
    game.block = block
    game.body = body

    game.save()

    event = GameEvent(id, 'update')

    return event

@mutation.field("deleteGame")
@database_sync_to_async
def resolve_delete_game(_, info, id):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("You can't do that!")

    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        logger.debug("Game not found")
        raise Exception("Game not found")

    game.delete()

    event = GameEvent(id, 'delete')

    return event
