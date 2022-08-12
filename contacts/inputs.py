# youbee_contacts/contacts/inputs.py

# System libraries

# Third-party libraries
import graphene

# Django modules

# Django apps

#  Current app modules


class PersonGroupInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    entity = graphene.ID(required=True)


class PersonTitleInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    entity = graphene.ID(required=True)


class PersonInput(graphene.InputObjectType):
    title = graphene.ID(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)