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

from schema import schema

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = URLRouter(
    [
        path("graphql/", GraphQL(schema, debug=True)),
        re_path(r"", get_asgi_application()),
    ]
)

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