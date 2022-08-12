# youbee_contacts/contacts/mutations.py

# System libraries

# Third-party libraries
import graphene
from graphql.error import GraphQLError

# Django modules
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Django apps

#  Current app modules
from .types import PersonGroupType, PersonTitleType
from .inputs import PersonGroupInput, PersonTitleInput
from .models import PersonGroup, PersonTitle
from .mixins import MutationInfoMixin


class CreatePersonGroup(graphene.Mutation, MutationInfoMixin):
    class Arguments:
        data = PersonGroupInput(required=True)

    person_group = graphene.Field(PersonGroupType)

    @classmethod
    def mutate(cls, root, info, data=None):
        try:
            person_group = PersonGroup.objects.create(name=data.name, entity=data.entity)
        except IntegrityError as e:
            return CreatePersonGroup(error=e, success=False)
        else:
            return CreatePersonGroup(person_group=person_group, success=True)


class CreatePersonGroupMasterList(graphene.Mutation, MutationInfoMixin):
    class Arguments:
        entity = graphene.ID(required=True)

    person_groups_list = graphene.List(PersonGroupType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        to = kwargs['entity']

        if to:
            PersonGroup.create_groups_list(to=to)

            pgl = PersonGroup.objects.filter(entity=to)
            return CreatePersonGroupMasterList(success=True, person_groups_list=pgl)
        else:
            return GraphQLError(message='No entity specified')


class DeleteItem(graphene.Mutation, MutationInfoMixin):
    class Arguments:
        group_id = graphene.ID()
        title_id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            if len(kwargs) == 0:
                raise ValueError('Nothing to delete')

            if kwargs.get('group_id'):
                PersonGroup.objects.filter(pk=kwargs.get('group_id')).delete()

            if kwargs.get('title_id'):
                PersonTitle.objects.filter(pk=kwargs.get('title_id')).delete()

            return DeleteItem(success=True)

        except Exception as e:
            return DeleteItem(success=False, error=e)


class CreatePersonTitle(graphene.Mutation, MutationInfoMixin):
    class Arguments:
        data = PersonTitleInput(required=True)

    person_title = graphene.Field(PersonTitleType)

    @classmethod
    def mutate(cls, root, info, data=None):
        try:
            pt = PersonTitle.objects.create(title=data.title, entity=data.entity)
        except IntegrityError as e:
            return CreatePersonTitle(error=e, success=False)
        else:
            return CreatePersonTitle(person_title=pt, success=True)


class CreatePersonTitleMasterList(graphene.Mutation, MutationInfoMixin):
    class Arguments:
        entity = graphene.ID(required=True)

    person_titles_list = graphene.List(PersonTitleType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        to = kwargs['entity']

        if to:
            PersonTitle.create_titles_list(to=to)

            ptl = PersonTitle.objects.filter(entity=to)
            return CreatePersonTitleMasterList(success=True, person_titles_list=ptl)
        else:
            return GraphQLError(message='No entity specified')


class Mutation(graphene.ObjectType):
    create_person_group = CreatePersonGroup.Field()
    create_person_group_master_list = CreatePersonGroupMasterList.Field()
    create_person_title = CreatePersonTitle.Field()
    create_person_title_master_list = CreatePersonTitleMasterList.Field()
    delete_item = DeleteItem.Field()


schema = graphene.Schema(mutation=Mutation)
