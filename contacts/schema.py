# youbee_contacts/contacts/schema.py

# System libraries

# Third-party libraries
import graphene

# Django modules

# Django apps

#  Current app modules
from .queries import schema as sq
from .mutations import schema as sm


class Query(sq.Query, graphene.ObjectType):
    pass


class Mutation(sm.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
