# youbee_contacts/management/commands/tests/test_builders.py

# System libraries

# Third-party libraries
import pytest

# Django modules

# Django apps
from contacts.models import PersonGroup, PersonTitle, Person
from contacts.constants import PERSON_GROUPS_MASTER_LIST, PERSON_TITLES_MASTER_LIST

#  Current app modules
from ..constants import STANDARD_DEPARTMENT_COUNT, STANDARD_EMPLOYEE_COUNT, STANDARD_CONTACT_COUNT
from ..builders import ContactBuilder, DatabaseEngineer


class BaseTestBuilder:
    @pytest.fixture
    def cb(self, db):
        return ContactBuilder(1)


class TestContactBuilder(BaseTestBuilder):
    def test_init(self, cb):  # test passed
        assert cb.entity_id == '1'
        assert cb.contact_count == STANDARD_CONTACT_COUNT
        assert cb.department_count == STANDARD_DEPARTMENT_COUNT
        assert cb.employee_count == STANDARD_EMPLOYEE_COUNT

    def test_set_entity_id(self, cb):  # test passed
        new_id = '2'
        assert cb.set_entity_id(new_id) == new_id
        assert cb.entity_id == new_id
        assert PersonGroup.objects.filter(entity=new_id).count() == len(PERSON_GROUPS_MASTER_LIST)
        assert PersonTitle.objects.filter(entity=new_id).count() == len(PERSON_TITLES_MASTER_LIST)

    def test_set_department_count_correct(self, cb):  # test passed
        new_value = expected_value = 4
        assert cb.set_department_count(new_value) == expected_value
        assert cb.department_count == expected_value

    def test_set_department_count_too_low(self, cb):  # test passed
        new_value = 1
        assert cb.set_department_count(new_value) == STANDARD_DEPARTMENT_COUNT
        assert cb.department_count == STANDARD_DEPARTMENT_COUNT

    def test_set_department_count_too_high(self, cb):  # test passed
        new_value = 7
        assert cb.set_department_count(new_value) == STANDARD_DEPARTMENT_COUNT
        assert cb.department_count == STANDARD_DEPARTMENT_COUNT

    def test_set_contact_count_correct(self, cb):  # test passed
        new_value = expected_value = 15
        assert cb.set_contact_count(new_value) == expected_value
        assert cb.contact_count == expected_value

    def test_set_contact_count_too_low(self, cb):  # test passed
        new_value = 1
        assert cb.set_contact_count(new_value) == STANDARD_CONTACT_COUNT
        assert cb.contact_count == STANDARD_CONTACT_COUNT

    def test_set_contact_count_too_high(self, cb):  # test passed
        new_value = 70
        assert cb.set_contact_count(new_value) == STANDARD_CONTACT_COUNT
        assert cb.contact_count == STANDARD_CONTACT_COUNT

    def test_set_employee_count_correct(self, cb):  # test passed
        new_value = expected_value = 10
        assert cb.set_employee_count(new_value) == expected_value
        assert cb.employee_count == expected_value

    def test_set_employee_count_too_low(self, cb):  # test passed
        assert cb.set_employee_count(4) == STANDARD_EMPLOYEE_COUNT
        assert cb.employee_count == STANDARD_EMPLOYEE_COUNT

    def test_set_employee_count_too_high(self, cb):  # test passed
        assert cb.set_employee_count(25) == STANDARD_EMPLOYEE_COUNT
        assert cb.employee_count == STANDARD_EMPLOYEE_COUNT

    def test_fake_person_data(self, cb):   # test passed
        data = cb.fake_person_data()
        assert data is not None
        assert data['title'] is not None
        assert data['first_name'] != ''
        assert data['last_name'] != ''
        assert data['gender'] != ''
        assert data['partner'] != ''
        assert data['group'] is not None
        assert data['created_by'] != ''
        assert data['entity'] != ''
        assert data['department'] != ''

    def test_fake_phone_number(self, cb):
        data = cb.fake_person_phone_number()
        assert data['phone_number'] is not None

    def test_fake_email_address(self, cb):
        data = cb.fake_person_email_address()
        assert data['email_address'] is not None

    def test_fake_location(self, cb):
        data = cb.fake_person_location()
        assert data is not None
        assert data['address'] is not None
        assert data['city'] is not None
        assert data['country'] is not None
        assert data['zip_code'] is not None
        assert data['phone'] is not None

    def test_fake_organisation(self, cb):
        data = cb.fake_person_organisation()
        assert data['organisation'] is not None
        assert data['organisation']['name'] is not None
        assert data['organisation']['nickname'] is not None
        assert data['organisation']['phone_number'] is not None
        assert data['organisation']['web_site'] is not None
        assert data['organisation']['location'] is not None

    def test_fake_function(self, cb):
        data = cb.fake_person_function()
        assert data['function'] is not None

    def test_get_random_group(self, cb):
        assert cb.get_random_group() is not None

    def test_get_random_title(self, cb):
        assert cb.get_random_title() is not None

    def test_get_random_department_id(self, cb):
        assert cb.get_random_department_id() is not None

    def test_get_random_employee_id(self, cb):
        assert cb.get_random_employee_id() is not None

    def test_build_contact(self, cb):
        cb.set_entity_id(1)
        c = cb.build_contact()
        assert c is not None

    def test_build(self, cb):
        cb.set_entity_id(1)
        n = cb.build()
        assert Person.objects.all().count() == n


class TestDatabaseEngineer:  # tests passed
    # test passed
    def test_construct_contact_book_defaults(self, db):
        deng = DatabaseEngineer()
        cbook = deng.construct_contact_book(entity_id=1)
        assert Person.objects.all().count() == cbook

