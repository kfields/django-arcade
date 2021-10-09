from loguru import logger

from channels.db import database_sync_to_async

#from .hub import hub, PlayerSubscriber, PlayerEvent
#from games.hub import hub as gamehub, JoinGameEvent

#from .hub import hub, GameSubscriber

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