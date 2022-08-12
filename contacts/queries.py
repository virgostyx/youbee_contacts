# youbee_contacts/contacts/queries.py

# System libraries

# Third-party libraries
import graphene
from graphene_django.debug import DjangoDebug
from graphql.error import GraphQLError

# Django modules
from django.core.exceptions import ObjectDoesNotExist
# Django apps

#  Current app modules
from .types import PersonGroupType, PersonTitleType
from .models import PersonGroup, PersonTitle


class Query(graphene.ObjectType):
    person_groups_list = graphene.List(PersonGroupType, entity=graphene.ID())
    person_group = graphene.Field(PersonGroupType, group_id=graphene.ID())
    person_titles_list = graphene.List(PersonTitleType, entity=graphene.ID())
    person_title = graphene.Field(PersonTitleType, title_id=graphene.ID())
    debug = graphene.Field(DjangoDebug, name='_debug')

    @staticmethod
    def resolve_person_group(root, info, **kwargs):
        group_id = kwargs.get('group_id')

        if group_id:
            try:
                pg = PersonGroup.objects.get(pk=group_id)
            except ObjectDoesNotExist:
                return GraphQLError(message='The group does not exist')
            else:
                return pg
        else:
            return PersonGroup.objects.none()

    @staticmethod
    def resolve_person_groups_list(root, info, **kwargs):
        #        if info.context.user.is_authenticated():
        entity = kwargs.get('entity')

        if entity:
            q = PersonGroup.objects.filter(entity=entity).defer('entity').order_by('name')

            return q if q.exists() else GraphQLError(message='The resulting list is empty')
        else:
            return PersonGroup.objects.none()

    @staticmethod
    def resolve_person_title(root, info, **kwargs):
        title_id = kwargs.get('title_id')

        if title_id:
            try:
                pt = PersonTitle.objects.get(pk=title_id)
            except ObjectDoesNotExist:
                return GraphQLError(message='The title does not exist')
            else:
                return pt
        else:
            return PersonTitle.objects.none()

    @staticmethod
    def resolve_person_titles_list(root, info, **kwargs):
        #        if info.context.user.is_authenticated():
        entity = kwargs.get('entity')

        if entity:
            q = PersonTitle.objects.filter(entity=entity).defer('entity').order_by('title')

            return q if q.exists() else GraphQLError(message='The resulting list is empty')
        else:
            return PersonTitle.objects.none()


schema = graphene.Schema(query=Query)
