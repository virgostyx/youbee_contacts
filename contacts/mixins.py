# youbee_contacts/contacts/mixins.py

# System libraries

# Third-party libraries
import graphene

# Django modules
from django.db import models

# Django apps

#  Current app modules


class RegistrationDataMixin:

    created_by = models.PositiveBigIntegerField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.PositiveBigIntegerField(editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)


class MutationInfoMixin:

    success = graphene.Boolean()
    error = graphene.String()
