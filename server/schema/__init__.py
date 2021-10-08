import os

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
    upload_scalar
)

from django.conf import settings

from .types import object_types

from .query import query
from .mutation import mutation
from .subscription import subscription

from games.hub import game_event

types = [game_event, query, mutation, subscription]

type_defs = load_schema_from_path(
    os.path.join(settings.BASE_DIR, "schema", "schemas")
)

#schema = make_executable_schema(type_defs, types, object_types, snake_case_fallback_resolvers, upload_scalar)
schema = make_executable_schema(type_defs, types, snake_case_fallback_resolvers, upload_scalar)
