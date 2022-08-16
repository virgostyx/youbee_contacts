# youbee_contacts/contacts/mixins.py

# System libraries

# Third-party libraries
import graphene

# Django modules
from django.db import models

# Django apps

#  Current app modules


class MutationInfoMixin:

    success = graphene.Boolean()
    error = graphene.String()
