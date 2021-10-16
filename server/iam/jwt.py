import jwt
import datetime
from loguru import logger

from channels.db import database_sync_to_async

from django.conf import settings
from users.models import User

SECRET_KEY = settings.SECRET_KEY


def encode_auth_token(**kwargs):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=0),
        "iat": datetime.datetime.utcnow(),
    }

    for key, value in kwargs.items():
        payload[key] = value

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def load_user(info):
    request = info.context["request"]
    token = decode_auth_token(request)
    logger.debug(f'load_user:token:  {token}')
    return User.objects.get(id=token["id"])


def decode_auth_token(scope):
    #logger.debug(f"jwt:decode:scope:  {scope}")
    headers = dict(scope['headers'])
    if not b'authorization' in headers:
        return None

    auth_token = headers[b'authorization'].decode()
    if auth_token.startswith("Bearer "):
        auth_token = auth_token.split(" ", 1)[1]
    logger.debug(f"jwt:decode:  {auth_token}")
    if not auth_token:
        auth_token = ""
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        message = f"Invalid token {auth_token}. Please log in again."
        logger.debug(f"jwt:decode:  {message}, secret:  {SECRET_KEY}")
        return message

'''
class JSONWebTokenMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        token = get_token_from_http_header(request)
        if token is not None:
            user = getattr(request, "user", None)
            if user is None or isinstance(user, AnonymousUser):
                user = authenticate(request=request, token=token)
            if user is not None:
                setattr(request, "user", user)
        return next(root, info, **kwargs)
'''

'''
    request = info.context["request"]
    token = decode_auth_token(request)
    logger.debug(f'load_user:token:  {token}')
    return User.objects.get(id=token["id"])
'''

'''
class JwtMiddleware:
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        token = decode_auth_token(request)
        logger.debug(f'load_user:token:  {token}')
        user = User.objects.get(id=token["id"])
        if not user.is_authenticated:
            raise Exception("User not authenticated")
        setattr(request, "user", user)
        return next(root, info, **kwargs)
'''
@database_sync_to_async
def authenticate(info):
    request = info.context["request"]
    token = decode_auth_token(request)
    logger.debug(f'authenticate:token:  {token}')
    return User.objects.get(id=token["id"])

async def jwt_middleware(resolver, obj, info, **args):
    request = info.context["request"]
    scope = request.scope
    #logger.debug(request)
    #logger.debug(resolver)
    #token = decode_auth_token(request)
    auth_token = request.headers.get("Authorization")
    if auth_token:
        user = await authenticate(info)
        scope["auth"] = user
    return resolver(obj, info, **args)
