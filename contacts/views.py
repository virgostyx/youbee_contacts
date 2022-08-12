# youbee_contacts/contacts/queries.py

# System libraries

# Third-party libraries
from graphene_django.views import  GraphQLView

# Django modules
from django.contrib.auth.mixins import LoginRequiredMixin

# Django apps

#  Current app modules


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

