from loguru import logger

from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from .jwt import decode_auth_token
from users.models import User

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, app):
        self.app = app

    @database_sync_to_async
    def get_user(self, id):
        user = User.objects.get(id=id)
        close_old_connections()
        return user

    async def __call__(self, scope, receive, send):
        token = decode_auth_token(scope)
        if token:
            logger.debug(f'load_user:token:  {token}')
            #user = await database_sync_to_async(User.objects.get)(id=token["id"])
            user = await self.get_user(token["id"])
        else:
            user = AnonymousUser()
        scope['user'] = user
        return await self.app(scope, receive, send)

TokenAuthMiddlewareStack = lambda app: TokenAuthMiddleware(AuthMiddlewareStack(app))

'''
class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
'''