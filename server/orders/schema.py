import asyncio

from loguru import logger

from ariadne import gql, make_executable_schema
from ariadne import QueryType, MutationType, SubscriptionType
from ariadne.contrib.django.scalars import date_scalar

from channels.db import database_sync_to_async

from orders.models import Order

query = QueryType()
mutation = MutationType()
subscription = SubscriptionType()

type_defs = gql(
    """
        scalar Date
        
        enum OrderState {
            PAID
            UNPAID
        }
        
        type User {
            username: String
            email: String
        }
        
        type Order {
            date: Date
            state: OrderState
            user: User
        }
        
        type Query {
            getOrders: [Order]
            getMessage: String!
        }
        
        type Subscription {
            getOrder: Order
            counter: Int
        }
"""
)
    
@query.field("getMessage")
def resolve_message(*_):
    logger.debug('resolve_message')
    return "Hello!"

@subscription.source("getOrder")
async def generate_order(obj, info):
    logger.debug('generate_order')
    while True:
        await asyncio.sleep(1)
        yield await database_sync_to_async(lambda: Order.objects.last())()

@subscription.field("getOrder")
def resolve_order(order, info):
    logger.debug('resolve_order')
    return order

@subscription.source("counter")
async def generate_counter(obj, info):
    logger.debug('generate_counter')
    count = 0
    while True:
        await asyncio.sleep(1)
        yield count
        count += 1

@subscription.field("counter")
def resolve_order(counter, info):
    logger.debug('counter')
    return counter


schema = make_executable_schema(type_defs, [date_scalar], query, subscription)