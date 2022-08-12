# youbee_contacts/contacts/tests/tests_person_groups.py

# System libraries
import json

# Third-party libraries
import pytest

# Django modules
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Django apps

#  Current app modules
from ..models import PersonGroup

CREATE_PERSON_GROUP_MUTATION = """
    mutation {
      createPersonGroup(data: {name: "new_group", entity: "1"}) {
        personGroup {
          name
        }
        success
        error
      }
    }
"""
DELETE_PERSON_GROUP_MUTATION = """
    mutation DeleteItemMutation($id: ID) {
      deleteItem(groupId: $id) {
        success
        error
      }
    }
"""
CREATE_PERSON_GROUP_MASTER_LIST = """
    mutation CreatePersonGroupMasterList($to: ID!) {
      createPersonGroupMasterList(entity: $to) {
        personGroupsList {
          name
        }
        success
        error
      }
    }
"""


@pytest.mark.django_db
class TestPersonGroupMutations:
    def test_create_new_person_group_not_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MUTATION)
        content = json.loads(response.content)
        assert 'errors' in content

    def test_create_new_person_group_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MUTATION)
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 1

    def test_create_existing_person_group_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MUTATION)
        content = json.loads(response.content)
        assert 'errors' not in content

        response = client_query(query=CREATE_PERSON_GROUP_MUTATION)
        content = json.loads(response.content)
        assert 'errors' in content

    def test_delete_person_group(self, client_query):
        pg = PersonGroup.objects.create(name='new_group', entity='1')
        assert PersonGroup.objects.count() == 1
        response = client_query(query=DELETE_PERSON_GROUP_MUTATION, variables={'id': pg.pk})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 0

    def test_create_person_group_master_list_for_an_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 10

    def test_create_person_group_master_list_without_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList')
        content = json.loads(response.content)
        assert 'errors' in content


GET_ALL_PERSON_GROUPS_FOR_AN_ENTITY = """
    query GetAllPersonGroupsForEntity($for: ID!) {
        personGroupsList(entity: $for) {
            id
            name
        }
    }
"""
GET_PERSON_GROUP_BY_ID = """
    query GetPersonGroupById($id: ID!) {
        personGroup(groupId: $id) {
            name
        }
    }
"""


@pytest.mark.django_db
class TestPersonGroupQueries:
    def test_get_all_person_groups_for_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 10
        response = client_query(query=GET_ALL_PERSON_GROUPS_FOR_AN_ENTITY,
                                op_name='GetAllPersonGroupsForEntity',
                                variables={'for': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_person_group_by_id(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 10
        response = client_query(query=GET_PERSON_GROUP_BY_ID,
                                op_name='GetPersonGroupById',
                                variables={'id': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_all_person_groups_for_non_existing_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 10
        response = client_query(query=GET_ALL_PERSON_GROUPS_FOR_AN_ENTITY,
                                op_name='GetAllPersonGroupsForEntity',
                                variables={'for': '2'})
        content = json.loads(response.content)
        assert 'errors' in content

    def test_get_person_group_non_existing(self, client_query):
        response = client_query(query=CREATE_PERSON_GROUP_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonGroup.objects.count() == 10
        response = client_query(query=GET_PERSON_GROUP_BY_ID,
                                op_name='GetPersonGroupById',
                                variables={'id': '110'})
        content = json.loads(response.content)
        assert 'errors' in content
