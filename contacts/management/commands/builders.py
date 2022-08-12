# youbee_contacts/contacts/management/commands/builders.py

# System libraries

# Third-party libraries

# Django modules

# Django apps
from contacts.models import PersonTitle, PersonGroup

#  Current app modules
from .base_builder import BaseFakeDataBuilder
from .constants import MIN_DEPARTMENT_COUNT, STANDARD_DEPARTMENT_COUNT, MAX_DEPARTMENT_COUNT, \
    MIN_CONTACT_COUNT, STANDARD_CONTACT_COUNT, MAX_CONTACT_COUNT, \
    MIN_EMPLOYEE_COUNT, STANDARD_EMPLOYEE_COUNT, MAX_EMPLOYEE_COUNT


class ContactBuilder(BaseFakeDataBuilder):
    entity_id = None
    group_count = None
    title_count = None

    def __init__(self, entity_id=None):
        super().__init__()

        self.department_count = STANDARD_DEPARTMENT_COUNT
        self.contact_count = STANDARD_CONTACT_COUNT
        self.employee_count = STANDARD_EMPLOYEE_COUNT

        if entity_id:
            self.set_entity_id(entity_id)

        return

    def set_entity_id(self, entity_id):
        self.entity_id = entity_id
        PersonGroup.create_groups_list(self.entity_id)
        self.group_count = PersonGroup.objects.filter(entity=self.entity_id).count()
        PersonTitle.create_titles_list(self.entity_id)
        self.title_count = PersonTitle.objects.filter(entity=self.entity_id).count()
        return self.entity_id

    def set_department_count(self, new_count):
        self.department_count = new_count if MIN_DEPARTMENT_COUNT < new_count < MAX_DEPARTMENT_COUNT \
                                          else STANDARD_DEPARTMENT_COUNT
        return self.department_count

    def set_contact_count(self, new_count):
        self.contact_count = new_count if MIN_CONTACT_COUNT < new_count < MAX_CONTACT_COUNT else STANDARD_CONTACT_COUNT
        return self.contact_count

    def set_employee_count(self, new_count):
        self.employee_count = new_count if MIN_EMPLOYEE_COUNT < new_count < MAX_EMPLOYEE_COUNT \
                                        else STANDARD_EMPLOYEE_COUNT
        return self.employee_count

    def fake_person_data(self):
        person_details = {
            'title': self.get_random_title(),
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'gender': self.faker.random_choices(elements=('M', 'F', 'U')),
            'partner': self.faker.random_choices(elements=('M', 'F', 'S', 'U')),
            'group': self.get_random_group(),
            'created_by': self.get_random_employee_id(),
            'entity': self.entity_id,
            'department': self.get_random_department_id(),
        }

        return person_details

    def get_random_group(self):
        return str(self.faker.random_int(min=1, max=self.group_count))

    def get_random_title(self):
        return str(self.faker.random_int(min=1, max=self.title_count))

    def get_random_department_id(self):
        return str(self.faker.random_int(min=1, max=self.department_count))

    def get_random_employee_id(self):
        return str(self.faker.random_int(min=1, max=self.employee_count))

    def build(self):
        return


class DatabaseEngineer:
    def __init__(self):
        self.builder = None

    def construct_contact_book(self,
                               entity_id,
                               contact_count=STANDARD_CONTACT_COUNT,
                               department_count=STANDARD_DEPARTMENT_COUNT,
                               employee_count=STANDARD_EMPLOYEE_COUNT):

        self.builder = ContactBuilder()
        self.builder.set_entity_id(entity_id)

        if department_count is not None:
            self.builder.set_department_count(department_count)

        if employee_count is not None:
            self.builder.set_employee_count(employee_count)

        return self.builder.build()

    @property
    def contact(self):
        return self.builder.contact
