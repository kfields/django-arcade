from loguru import logger

from channels.db import database_sync_to_async

#from .hub import hub, PlayerSubscriber, PlayerEvent
from games.hub import hub as gamehub, JoinEvent

from schema.base import mutation
from users.jwt import load_user
from .models import Player, Game

@database_sync_to_async
def sync_resolve_join_game(_, info, gameId):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")
    game = Game.objects.get(id=gameId)

    if Player.objects.filter(user=user, game=game).exists():
        player = Player.objects.get(user=user, game=game)
    #else
    elif len(Player.objects.filter(game=game)) == 0:
        player = Player.objects.create(user=user, game=game, symbol='X')
    else:
        player = Player.objects.create(user=user, game=game, symbol='O')

    return player, gameId

@mutation.field("joinGame")
#async def resolve_join_game(_, info, gameId):
async def resolve_join_game(*args, **kwargs):
    player, gameId = await sync_resolve_join_game(*args, **kwargs)
    event = JoinEvent(gameId, player.id)
    await gamehub.send(event)
    return player


'''
@mutation.field("updatePlayer")
@database_sync_to_async
def resolve_update_player(_, info, id, data):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")

    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        logger.debug("Player not found")
        raise Exception("Player not found")

    title = data.get("title", None)
    block = data.get("block", None)
    body = data.get("body", None)

    player.title = title
    player.block = block
    player.body = body

    player.save()

    event = PlayerEvent(id, 'update')

    return event

@mutation.field("deletePlayer")
@database_sync_to_async
def resolve_delete_player(_, info, id):
    user = load_user(info)
    if not user.is_authenticated:
        raise Exception("User not authenticated")

    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        logger.debug("Player not found")
        raise Exception("Player not found")

    player.delete()

    event = PlayerEvent(id, 'delete')

    return event
'''