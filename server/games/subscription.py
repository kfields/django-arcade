import asyncio

from loguru import logger

from schema.base import subscription
from .hub import hub, GameSubscriber

@subscription.source("game")
async def events_generator(obj, info, id=None):
    logger.debug(f'events_generator:begin:id {id}')
    subscriber = GameSubscriber(int(id))
    hub.subscribe(subscriber)
    while subscriber.active:
        event = await subscriber.receive()
        logger.debug(f'events_generator:while:  {event}')
        yield event

@subscription.field("game")
def events_resolver(event, info, id=None):
    logger.debug(f'events_resolver:while:  {event}')
    return event
