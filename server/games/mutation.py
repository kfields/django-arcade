from loguru import logger

from channels.db import database_sync_to_async

from django_arcade_core.game_event import GameEvent, JoinGameEvent

from schema.base import mutation
from users.jwt import load_user
from .models import Game
from .hub import hub


@mutation.field("createGame")
@database_sync_to_async
def resolve_create_game(_, info):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")

    game = Game.objects.create()

    return game

@mutation.field("updateGame")
@database_sync_to_async
def resolve_update_game(_, info, id, data):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")

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
        raise Exception("User not authenticated")

    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        logger.debug("Game not found")
        raise Exception("Game not found")

    game.delete()

    event = GameEvent(id, 'delete')

    return event

@database_sync_to_async
def sync_resolve_join_game(_, info, gameId):
    game = Game.objects.get(id=gameId)

    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")
    '''
    if Player.objects.filter(user=user, game=game).exists():
        player = Player.objects.get(user=user, game=game)
    #else
    elif len(Player.objects.filter(game=game)) == 0:
        player = Player.objects.create(user=user, game=game, symbol='X')
    else:
        player = Player.objects.create(user=user, game=game, symbol='O')
    '''
    player = game.join(user)
    return player, gameId

@mutation.field("joinGame")
async def resolve_join_game(*args, **kwargs):
    player, gameId = await sync_resolve_join_game(*args, **kwargs)
    logger.debug(f'resolve_join_game:player_id:  {player.id}')
    event = JoinGameEvent(gameId, player.id)
    await hub.send(event)
    return player
