# youbee_main/fixtures/builders/tests/test_base_builder.py

# System libraries

# Third-party libraries

# Django modules

# Django apps

#  Current app modules
import pytest

from ..base_builder import BaseContactBuilder


class TestBaseContactBuilder:  # tests passed
    @pytest.fixture
    def beb(self):
        beb = BaseContactBuilder()
        return beb

    def test_init(self, beb):
        assert beb.contact_builder is None

    def test_init_with_parameter(self):
        param = BaseContactBuilder()
        beb = BaseContactBuilder(param)
        assert beb.contact_builder == param

    def test_set_contact_builder(self, beb):
        param = BaseContactBuilder()
        beb.set_contact_builder(param)
        assert beb.contact_builder == param

    def test_init_faker(self, beb):
        assert beb.faker is not None
        assert type(beb.faker) is not 'faker.proxy.Faker'
