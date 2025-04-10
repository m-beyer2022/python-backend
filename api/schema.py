import strawberry

from .query import Query
from .mutation import Mutation

"""GraphQL Schema Definition

This module defines the root GraphQL schema for the Spotify API wrapper.
It combines all queries and mutations into a single schema object.
"""

schema = strawberry.Schema(query=Query, mutation=Mutation)
