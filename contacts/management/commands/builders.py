# youbee_contacts/contacts/management/commands/builders.py

# System libraries

# Third-party libraries
from phone_gen import PhoneNumber as pn

# Django modules

# Django apps
from contacts.models import PersonTitle, PersonGroup, Person, PhoneNumber, EmailAddress, Location, Organisation, \
    PersonFunction

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
        title_id = self.get_random_title()
        group_id = self.get_random_group()
        employee_id = self.get_random_employee_id()

        person_details = {
            'title': PersonTitle.objects.get(pk=title_id),
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'gender': self.faker.random_choices(elements=('M', 'F', 'U')),
            'partner': self.faker.random_choices(elements=('M', 'F', 'S', 'U')),
            'person_group': PersonGroup.objects.get(pk=group_id),
            'created_by': employee_id,
            'modified_by': employee_id,
            'entity': self.entity_id,
            'department': self.get_random_department_id(),
        }

        return person_details

    def fake_person_phone_number(self):
        phone_number = pn('GB')

        person_phone_number = {
            'person': '',
            'phone_number': phone_number.get_number(),
        }

        return person_phone_number

    def fake_person_email_address(self):
        person_email_address = {
            'person': '',
            'email_address': self.faker.ascii_email(),
        }

        return person_email_address

    def fake_person_location(self):
        country_code = self.faker.country_code()

        person_location = {
            'person': '',
            'address': self.faker.street_address(),
            'city': self.faker.city(),
            'country': country_code,
            'zip_code': self.faker.postcode(),
            'phone': pn(country_code).get_number()
        }

        return person_location

    def fake_organisation_location(self):
        country_code = self.faker.country_code()
        organisation_location = {
            'address': self.faker.street_address(),
            'city': self.faker.city(),
            'country': country_code,
            'zip_code': self.faker.postcode(),
            'phone': pn(country_code).get_national(),
            'person': '',
        }

        return organisation_location

    def fake_person_organisation(self):
        location = self.fake_organisation_location()
        person_organisation = {
            'organisation': {
                'name': self.faker.company(),
                'nickname': self.faker.catch_phrase(),
                'phone_number': pn(location['country']).get_national(),
                'email_address': self.faker.ascii_company_email(),
                'web_site': self.faker.url(),
                'person': '',
                'location': '',
            },
            'location': location,
        }
        return person_organisation

    def fake_person_function(self):
        person_function = {
            'function': self.faker.job(),
            'person': '',
        }
        return person_function

    def get_random_group(self):
        return self.faker.random_int(min=1, max=self.group_count)

    def get_random_title(self):
        return str(self.faker.random_int(min=1, max=self.title_count))

    def get_random_department_id(self):
        return self.faker.random_int(min=1, max=self.department_count)

    def get_random_employee_id(self):
        return self.faker.random_int(min=1, max=self.employee_count)

    def build_contact(self):
        # Create the new person
        new_contact = Person.objects.create(**self.fake_person_data())

        # Create the phone number of the person
        phone_number = self.fake_person_phone_number()
        phone_number['person'] = new_contact
        PhoneNumber.objects.get_or_create(**phone_number)

        # Create the person's email address
        email_address = self.fake_person_email_address()
        email_address['person'] = new_contact
        EmailAddress.objects.create(**email_address)

        # Create the person's location
        location = self.fake_person_location()
        location['person'] = new_contact
        p, _ = PhoneNumber.objects.get_or_create(person=new_contact, phone_number=location['phone'])
        location['phone'] = p
        Location.objects.create(**location)

        # Create the organisation the person belongs to
        organisation = self.fake_person_organisation()
        organisation['organisation']['person'] = new_contact
        p, _ = PhoneNumber.objects.get_or_create(person=new_contact, phone_number=organisation['organisation']['phone_number'])
        organisation['organisation']['phone_number'] = p
        organisation['location']['person'] = new_contact
        p, _ = PhoneNumber.objects.get_or_create(person=new_contact, phone_number=organisation['location']['phone'])
        organisation['location']['phone'] = p

        location = Location.objects.create(**organisation['location'])
        organisation['organisation']['location'] = location
        e, _ = EmailAddress.objects.get_or_create(person=new_contact, email_address=organisation['organisation']['email_address'])
        organisation['organisation']['email_address'] = e
        Organisation.objects.create(**organisation['organisation'])

        # Create the function of the person
        person_function = self.fake_person_function()
        person_function['person'] = new_contact
        PersonFunction.objects.create(**person_function)

        return new_contact

    def build(self):
        for _ in range(self.contact_count):
            self.build_contact()

        return self.contact_count


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

        if contact_count is not None:
            self.builder.set_contact_count(contact_count)

        return self.builder.build()
