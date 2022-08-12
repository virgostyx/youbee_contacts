# youbee_contacts/contacts/types.py

# System libraries

# Third-party libraries
from graphene_django import DjangoObjectType

# Django modules

# Django apps

#  Current app modules
from .models import Person, PersonGroup, PersonTitle, PhoneNumber, EmailAddress


class PersonGroupType(DjangoObjectType):
    class Meta:
        model = PersonGroup
        fields = ['id', 'name', ]


class PersonTitleType(DjangoObjectType):
    class Meta:
        model = PersonTitle
        fields = ['id', 'title', ]


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ['id',
                  'title',
                  'first_name',
                  'last_name',
                  'gender',
                  'partner',
                  'person_group',
                  'owner_entity',
                  'owner_department', ]


class PhoneNumberType(DjangoObjectType):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number', ]


class EmailAddressType(DjangoObjectType):
    class Meta:
        model = EmailAddress
        fields = ['id', 'email_address', ]
