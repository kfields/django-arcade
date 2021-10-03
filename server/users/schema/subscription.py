import asyncio

from schema.types.base import subscription
from users.models import User

@subscription.source("counter")
async def generate_counter(obj, info):
    count = 0
    while True:
        await asyncio.sleep(1)
        yield count
        count += 1

@subscription.field("counter")
def resolve_counter(counter, info):
    return counter

@subscription.source("counter2")
async def generate_counter2(obj, info):
    count = 10
    while True:
        await asyncio.sleep(1)
        yield count
        count += 1

@subscription.field("counter2")
def resolve_counter2(counter, info):
    return counter
