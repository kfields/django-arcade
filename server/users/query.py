from channels.db import database_sync_to_async

from schema.types.base import query
from users.models import User
from . import UserConnection

@query.field("getMessage")
def resolve_message(*_):
    return "Hello!"

@query.field("allUsers")
@database_sync_to_async
def resolve_all_users(root, info, after='', before='', first=0, last=0):
    users = [u for u in User.objects.all()]
    connection = UserConnection(users)
    result = connection.wire()
    return result

@query.field("user")
@database_sync_to_async
def resolve_user(*_, id):
    return User.objects.get(id=id)
