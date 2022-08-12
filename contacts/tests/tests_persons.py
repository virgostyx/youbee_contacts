# youbee_contacts/contacts/tests/tests_person_titles.py

# System libraries
import json

# Third-party libraries
import pytest

# Django modules

# Django apps

#  Current app modules
from ..models import Person

CREATE_PERSON_MUTATION = """
    mutation createPersonMutation($input: PersonInput!) {
      createPerson(data: $input) {
        person {
          id
          title
          first_name
          last_name
          gender
          partner
          person_group
          owner_entity
          owner_department
        }
        success
        error
      }
    }
"""
DELETE_PERSON_MUTATION = """
    mutation DeleteItemMutation($id: ID) {
      deleteItem(titleId: $id) {
        success
        error
      }
    }
"""


@pytest.mark.django_db
class TestPersonMutations:
    def test_create_new_person(self, client_query):
        input_data = {'title': '1',
                      'first_name': 'Tidiane',
                      'last_name': 'FIEVET',
                      'gender': 'M',
                      'partner': 'S',
                      'person_group': '1',
                      'owner_entity': '1',
                      'owner_department': '1',
                      }

        response = client_query(query=CREATE_PERSON_MUTATION,
                                op_name='createPersonMutation',
                                input_data=input_data)
        content = json.loads(response.content)
        assert 'errors' not in content
        assert Person.objects.count() == 1

    def test_create_existing_person(self, client_query):
        response = client_query(query=CREATE_PERSON_MUTATION)
        content = json.loads(response.content)
        assert 'errors' not in content

        response = client_query(query=CREATE_PERSON_MUTATION)
        content = json.loads(response.content)
        assert 'errors' in content

    def test_delete_person(self, client_query):
        pt = Person.objects.create(title='new_title', entity='1')
        assert Person.objects.count() == 1
        response = client_query(query=DELETE_PERSON_MUTATION, variables={'id': pt.pk})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert Person.objects.count() == 0


GET_ALL_PERSONS_FOR_AN_OWNER = """
    query GetAllPersonTitlesForEntity($for: ID!) {
        personTitlesList(entity: $for) {
            id
            title
        }
    }
"""
GET_PERSON_BY_ID = """
    query GetPersonTitleById($id: ID!) {
        personTitle(titleId: $id) {
            title
        }
    }
"""


@pytest.mark.django_db
class TestPersonQueries:
    @pytest.fixture()
    def create_person(self, client_query):
        response = client_query(query=CREATE_PERSON_MUTATION,
                                op_name='CreatePersonTitleMasterList',
                                variables={'to': '1'})
        assert Person.objects.count() == 1
        yield response

    def test_get_all_person_titles_of_owner(self, client_query, create_person):
        response = client_query(query=GET_ALL_PERSONS_FOR_AN_OWNER,
                                op_name='GetAllPersonTitlesForEntity',
                                variables={'for': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_person_by_id(self, client_query, create_person):
        response = client_query(query=GET_PERSON_BY_ID,
                                op_name='GetPersonTitleById',
                                variables={'id': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

