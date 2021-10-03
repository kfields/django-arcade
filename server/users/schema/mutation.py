from asgiref.sync import sync_to_async

from loguru import logger

from schema.types.base import mutation

from users.models import User
from users.jwt import encode_auth_token

@mutation.field("login")
@sync_to_async
def resolve_login(_, info, data):
    logger.debug(f"Login {data}")

    username = data['username']
    password = data['password']

    if not username:
        logger.debug("Username is missing")
        raise Exception('Username missing!')
    if not password:
        logger.debug("Password is missing")
        raise Exception('Password missing!')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user is None or not user.check_password(password):
        logger.debug("No such user or invalid password")
        raise Exception('No such user or invalid password!')

    # Identity can be any data that is json serializable
    access_token = encode_auth_token(sub=username, id=user.id)
    logger.debug(f"Access token: {access_token}")
    # token = json.dumps({"token": access_token.decode('utf-8')})
    #token = access_token.decode('utf-8')
    #logger.debug(f"Token: {token}")
    return {'token': access_token}

@mutation.field("register")
@sync_to_async
def resolve_register(_, info, data):
    logger.debug(f"registration {data}")

    username = data["username"]
    password = data["password"]
    email = data["email"]

    if not username or not password or not email:
        logger.info(f"Invalid registration data u:'{username}' p:'{password}' e:'{email}'")
        raise Exception("Invalid registration data")

    try:
        User.objects.get(username=username)
        raise Exception(f"Username {username} is already in use")
    except User.DoesNotExist:
        user = User.objects.create_user(username, email, password)
        user.save()
        return True
