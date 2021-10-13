"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from ariadne.asgi import GraphQL
from channels.routing import URLRouter
from django.urls import path, re_path


from users.auth import BasicAuthBackend
from schema import schema
from users.jwt import jwt_middleware
from iam.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def get_context_value(request):
    return {
        "request": request,
        "cookies": request.scope.get("cookies", {}),
        "user": request.scope.get("user"),
        "session": request.scope.get("session"),
    }

application = TokenAuthMiddleware(URLRouter(
    [
        #path("graphql/", GraphQL(schema, debug=True, middleware=[jwt_middleware])),
        path("graphql/", GraphQL(schema, debug=True, context_value=get_context_value)),
        re_path(r"", get_asgi_application()),
    ]
))

'''
import os

from django.core.asgi import get_asgi_application

from ariadne.asgi import GraphQL
from channels.http import AsgiHandler
from channels.routing import URLRouter
from django.urls import path, re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

#application = get_asgi_application()

from .schema import schema


application = URLRouter([
    path("graphql/", GraphQL(schema, debug=True)),
    re_path(r"", AsgiHandler),
])
'''