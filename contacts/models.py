# youbee_contacts/contacts/models.py

# System libraries
import uuid
from enum import Enum

# Third-party libraries
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from autoslug import AutoSlugField

# Django modules
from django.db import models

# Django apps

# Current-app modules
from .constants import PERSON_TITLES_MASTER_LIST, PERSON_GROUPS_MASTER_LIST


def _person_slug_fields(instance):
    return "{0}-{1}".format(instance.first_name, instance.last_name)


class AuditModel(models.Model):
    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.PositiveBigIntegerField(editable=False)
    modified_by = models.PositiveBigIntegerField(editable=False)


class PersonGroup(models.Model):
    class Meta:
        permissions = [('unlink_persongroup', 'Can unlink person group'), ]
        unique_together = [['entity', 'name']]
        ordering = ['entity', 'name']

    name = models.CharField(max_length=20, help_text='Important. Must be unique for your entity', verbose_name='group')
    entity = models.PositiveBigIntegerField(editable=False)

    @classmethod
    def create_groups_list(cls, to):

        for group in PERSON_GROUPS_MASTER_LIST:
            if not cls.objects.filter(entity=to, name=group).exists():
                cls.objects.create(entity=to, name=group)

    def __str__(self):
        return self.name


class PersonTitle(models.Model):
    class Meta:
        permissions = [('unlink_persontitle', 'Can unlink person title'), ]
        unique_together = [['entity', 'title']]
        ordering = ['entity', 'title']

    title = models.CharField(max_length=16)
    entity = models.PositiveBigIntegerField(editable=False)

    @classmethod
    def create_titles_list(cls, to):

        for title in PERSON_TITLES_MASTER_LIST:
            if not cls.objects.filter(entity=to, title=title).exists():
                cls.objects.create(entity=to, title=title)

    def __str__(self):
        return self.title


class Person(AuditModel):
    class Meta:
        permissions = [('unlink_person', 'Can unlink person'), ]
        unique_together = [['entity', 'first_name', 'last_name', 'sub_name']]
        ordering = ['last_name', 'first_name']

    class PARTNERS(Enum):

        male = ('M', 'Male')
        female = ('F', 'Female')
        single = ('S', 'Single')
        undefined = ('U', 'Undefined')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    class GENDERS(Enum):
        male = ('M', 'Male')
        female = ('F', 'Female')
        undefined = ('U', 'Undefined')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    STATUS = Choices('draft', 'confirmed')

    # Barcode data - automatic
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    # Required data
    title = models.ForeignKey(PersonTitle, on_delete=models.DO_NOTHING, verbose_name='title',
                              help_text='Critical. Please make sure it is correct')
    first_name = models.CharField(verbose_name='first name', max_length=32,
                                  help_text='Critical. Please make sure it is correct')
    last_name = models.CharField(verbose_name='last name', max_length=32,
                                 help_text='Critical. Please make sure it is correct')
    slug_name = AutoSlugField(populate_from=_person_slug_fields, max_length=64, editable=False, unique=True)

    # Other personal data
    sub_name = models.CharField(max_length=1, default='0', editable=False)
    gender = models.CharField(verbose_name='gender', max_length=1, default='U', choices=[x.value for x in GENDERS])
    partner = models.CharField(verbose_name='partner status', max_length=1, default='U',
                               choices=[x.value for x in PARTNERS])

    # Status data
    status = StatusField(default='draft', choices_name='STATUS', editable=False)
    status_changed = MonitorField(monitor='status', editable=False)
    confirmed_on = MonitorField(monitor='status', when=['confirmed'], editable=False)

    # Category data
    person_group = models.ForeignKey(PersonGroup, on_delete=models.DO_NOTHING, editable=False)

    # Owner data
    entity = models.PositiveBigIntegerField(editable=False)
    department = models.PositiveBigIntegerField(editable=False)

    @classmethod
    def get_next_sub_name(cls, owner_entity, first_name, last_name):
        return str(cls.objects.filter(owner_entity=owner_entity, last_name=last_name, first_name=first_name).count())

    def display_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name.upper())

    @property
    def full_name(self):
        return "{last_name}, {first_name}".format(first_name=self.first_name, last_name=self.last_name.upper())

    def __str__(self):
        return "{title} {first_name} {name}".format(
               title=self.title, first_name=self.first_name, name=self.last_name)


class PhoneNumber(models.Model):
    class Meta:
        unique_together = ['phone_number']
        ordering = ['phone_number']

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='phone_numbers')

    phone_number = PhoneNumberField()


class EmailAddress(models.Model):
    class Meta:
        unique_together = ['email_address']
        ordering = ['email_address']

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='email_addresses')

    email_address = models.EmailField()


class Location(models.Model):
    class Meta:
        ordering = ['address']

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='locations')

    # Location data
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=32, blank=True)
    country = CountryField(blank_label='(select country)', blank=True)
    zip_code = models.CharField(max_length=16, blank=True)

    phone = models.ForeignKey(PhoneNumber, on_delete=models.DO_NOTHING, related_name='location_phone_numbers')


class Organisation(models.Model):
    class Meta:
        unique_together = ['name']

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='organisations')

    name = models.CharField('name', max_length=200)
    nickname = models.CharField('nickname', max_length=50, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', max_length=64, unique=True)
    about = models.TextField('about', blank=True, null=True)

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.DO_NOTHING, related_name='organisation_phone_numbers')
    email_address = models.ForeignKey(EmailAddress, on_delete=models.DO_NOTHING, related_name='organisation_email_addresses')
    web_site = models.URLField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='organisation_locations')


class PersonFunction(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='functions')

    function = models.CharField(max_length=48, help_text='Important. Please make sure it is correct')