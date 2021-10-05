import os

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
    upload_scalar
)

from django.conf import settings

from .user import user

from .query import query
from .mutation import mutation
from .subscription import subscription

types = [user, query, mutation, subscription]

type_defs = load_schema_from_path(
    os.path.join(settings.BASE_DIR, "schema", "schemas")
)

schema = make_executable_schema(type_defs, types, snake_case_fallback_resolvers, upload_scalar)
