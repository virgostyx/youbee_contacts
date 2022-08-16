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
    @pytest.fixture
    def construct_data(self):
        return {
            'entity_name': None,
            'supervisor_email': None,
            'department_count': None,
            'manager_count': None,
            'employee_count': None,
        }

    # test passed
    def test_construct_entity_defaults(self, init_empty_db):
        deng = DatabaseEngineer()
        e = deng.construct_entity()
        assert e is not None
        assert Entity.objects.count() == 1
        assert e.departments.count() == DEPARTMENT_COUNT + 1
        assert e.employees.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 1

    # test passed
    def test_construct_entity_defaults_data(self, init_empty_db, construct_data):
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert Entity.objects.count() == 1
        assert e.departments.count() == DEPARTMENT_COUNT+1
        assert e.employees.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 1

    # test passed
    def test_construct_entity_with_entity_name(self, init_empty_db, construct_data):
        entity_name = 'The Youbee Test Company'
        construct_data['entity_name'] = entity_name
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert e.name == entity_name
        assert Entity.objects.count() == 1
        assert e.departments.count() == DEPARTMENT_COUNT+1
        assert e.employees.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 1

    # test passed
    def test_construct_entity_with_supervisor_email(self, init_empty_db, construct_data):
        supervisor_email = 'test.youbee+super@gmail.com'
        construct_data['supervisor_email'] = supervisor_email
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert e.supervisor.email == supervisor_email
        assert Entity.objects.count() == 1
        assert User.objects.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 2
        assert e.departments.count() == DEPARTMENT_COUNT+1
        assert e.employees.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 1

    # test passed
    def test_construct_entity_with_department_count(self, init_empty_db, construct_data):
        construct_data['department_count'] = 5
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert Entity.objects.count() == 1
        assert User.objects.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 2
        assert e.departments.count() == 6
        assert e.employees.count() == EMPLOYEE_COUNT + MANAGER_COUNT + 1

    # test passed
    def test_construct_entity_with_employee_count(self, init_empty_db, construct_data):
        construct_data['employee_count'] = 50
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert Entity.objects.count() == 1
        assert User.objects.count() == MANAGER_COUNT + 52
        assert e.departments.count() == DEPARTMENT_COUNT + 1
        assert e.employees.count() == MANAGER_COUNT + 51

    # test passed
    def test_construct_entity_with_manager_count(self, init_empty_db, construct_data):
        construct_data['manager_count'] = 2
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        assert e is not None
        assert Entity.objects.count() == 1
        assert User.objects.count() == EMPLOYEE_COUNT + 4
        assert e.departments.count() == DEPARTMENT_COUNT+1
        assert e.employees.count() == EMPLOYEE_COUNT + 3

    def test_construct_partnerships_with_defaults(self, init_empty_db, construct_data):
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        deng.construct_partnerships(entity=e)
        assert e.partners.count() == 2
        assert Partnership.objects.filter(leader=e).count() == 2

    def test_construct_partnerships_with_specified_count(self, init_empty_db, construct_data):
        deng = DatabaseEngineer()
        e = deng.construct_entity(**construct_data)
        deng.construct_partnerships(entity=e, partners_count=3)
        assert e.partners.count() == 3
        assert Partnership.objects.filter(leader=e).count() == 3

    # test passed
    def test_create_test_data(self, init_empty_db, construct_data):
        deng = DatabaseEngineer()
        entity_name = 'The Youbee Test Company'
        supervisor_email = 'test.youbee+super@gmail.com'
        construct_data['entity_name'] = entity_name
        construct_data['supervisor_email'] = supervisor_email
        e1 = deng.construct_entity(**construct_data)
        assert e1 is not None
        assert e1.name == entity_name
        assert e1.supervisor.email == supervisor_email
        assert Entity.objects.count() == 1
        construct_data['entity_name'] = None
        construct_data['supervisor_email'] = None
        e2 = deng.construct_entity(**construct_data)
        assert e2 is not None
        assert e2 is not e1
        assert Entity.objects.count() == 2
        e3 = deng.construct_entity(**construct_data)
        assert e3 is not None
        assert e3 is not e1 and e3 is not e2
        assert Entity.objects.count() == 3
        e4 = deng.construct_entity(department_count=6, manager_count=2, employee_count=50)
        assert e4 is not None
        assert e4 is not e1 and e4 is not e2 and e4 is not e1
        assert Entity.objects.count() == 4
        deng.construct_partnerships(e4)
        assert e4.partners.count() == 2
        assert Partnership.objects.all().count() == 2
