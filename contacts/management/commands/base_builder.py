# youbee_main/fixtures/builders/base_builder.py

# System libraries
import abc

# Third-party libraries
from faker import Faker

# Django modules

# Django apps

#  Current app modules


class BaseFakeDataBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self.faker = Faker()
        Faker.seed(0)

    @abc.abstractmethod
    def build(self):
        pass


class BaseContactBuilder(BaseFakeDataBuilder):
    def __init__(self, e_builder=None):
        super().__init__()
        self.contact_builder = e_builder

    def set_contact_builder(self, contact_builder=None):
        if contact_builder is not None:
            self.contact_builder = contact_builder

            return self.contact_builder

    def build(self):
        pass
