# youbee_contacts/contacts/tests/tests_person_titles.py

# System libraries
import json

# Third-party libraries
import pytest

# Django modules

# Django apps

#  Current app modules
from ..models import PersonTitle
from ..constants import PERSON_TITLES_MASTER_LIST

CREATE_PERSON_TITLE_MUTATION = """
    mutation {
      createPersonTitle(data: {title: "new_title", entity: "1"}) {
        personTitle {
          title
        }
        success
        error
      }
    }
"""
DELETE_PERSON_TITLE_MUTATION = """
    mutation DeleteItemMutation($id: ID) {
      deleteItem(titleId: $id) {
        success
        error
      }
    }
"""
CREATE_PERSON_TITLE_MASTER_LIST = """
    mutation CreatePersonTitleMasterList($to: ID!) {
      createPersonTitleMasterList(entity: $to) {
        personTitlesList {
          id
          title
        }
        success
        error
      }
    }
"""


@pytest.mark.django_db
class TestPersonTitleMutations:
    def test_create_new_person_title_not_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MUTATION)
        content = json.loads(response.content)
        assert 'errors' in content

    def test_create_new_person_title_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MUTATION)
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonTitle.objects.count() == 1

    def test_create_existing_person_title_authenticated(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MUTATION)
        content = json.loads(response.content)
        assert 'errors' not in content

        response = client_query(query=CREATE_PERSON_TITLE_MUTATION)
        content = json.loads(response.content)
        assert 'errors' in content

    def test_delete_person_title(self, client_query):
        pt = PersonTitle.objects.create(title='new_title', entity='1')
        assert PersonTitle.objects.count() == 1
        response = client_query(query=DELETE_PERSON_TITLE_MUTATION, variables={'id': pt.pk})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonTitle.objects.count() == 0

    def test_create_person_title_master_list_for_an_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MASTER_LIST,
                                op_name='CreatePersonTitleMasterList',
                                variables={'to': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content
        assert PersonTitle.objects.count() == len(PERSON_TITLES_MASTER_LIST)

    def test_create_person_title_master_list_without_entity(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MASTER_LIST,
                                op_name='CreatePersonGroupMasterList')
        content = json.loads(response.content)
        assert 'errors' in content


GET_ALL_PERSON_TITLES_FOR_AN_ENTITY = """
    query GetAllPersonTitlesForEntity($for: ID!) {
        personTitlesList(entity: $for) {
            id
            title
        }
    }
"""
GET_PERSON_TITLE_BY_ID = """
    query GetPersonTitleById($id: ID!) {
        personTitle(titleId: $id) {
            title
        }
    }
"""


@pytest.mark.django_db
class TestPersonTitleQueries:
    @pytest.fixture()
    def create_list(self, client_query):
        response = client_query(query=CREATE_PERSON_TITLE_MASTER_LIST,
                                op_name='CreatePersonTitleMasterList',
                                variables={'to': '1'})
        assert PersonTitle.objects.count() == len(PERSON_TITLES_MASTER_LIST)
        yield response

    def test_get_all_person_titles_for_entity(self, client_query, create_list):
        response = client_query(query=GET_ALL_PERSON_TITLES_FOR_AN_ENTITY,
                                op_name='GetAllPersonTitlesForEntity',
                                variables={'for': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_person_title_by_id(self, client_query, create_list):
        response = client_query(query=GET_PERSON_TITLE_BY_ID,
                                op_name='GetPersonTitleById',
                                variables={'id': '1'})
        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_all_person_titles_for_non_existing_entity(self, client_query, create_list):
        response = client_query(query=GET_ALL_PERSON_TITLES_FOR_AN_ENTITY,
                                op_name='GetAllPersonTitlesForEntity',
                                variables={'for': '2'})
        content = json.loads(response.content)
        assert 'errors' in content

    def test_get_person_group_non_existing(self, client_query, create_list):
        response = client_query(query=GET_PERSON_TITLE_BY_ID,
                                op_name='GetPersonTitleById',
                                variables={'id': '110'})
        content = json.loads(response.content)
        assert 'errors' in content
