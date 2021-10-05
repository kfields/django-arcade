import asyncio
from channels.db import database_sync_to_async

from schema.base import subscription
import users
from users.models import User

@subscription.source("counter")
@database_sync_to_async
async def generate_counter(obj, info):
    #count = 0
    while True:
        await asyncio.sleep(1)
        yield users.counter
        users.counter += 1

@subscription.field("counter")
@database_sync_to_async
def resolve_counter(counter, info):
    return counter

@subscription.source("counter2")
@database_sync_to_async
async def generate_counter2(obj, info):
    count = 10
    while True:
        await asyncio.sleep(1)
        yield count
        count += 1

@subscription.field("counter2")
@database_sync_to_async
def resolve_counter2(counter, info):
    return counter
