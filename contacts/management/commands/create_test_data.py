# entities/management/commands/create_test_data.py

# System libraries
import time

# Third-party libraries

# Django modules
from django.core.management.base import BaseCommand

# Django apps


# Current app modules
from .builders import DatabaseEngineer


SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(BaseCommand):
    help = "Create test data for n test contact books"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('-n', '--count', type=int, nargs='?', default=4)

    def handle(self, *args, **options):

        n = options['count']

        verbosity = options.get("verbosity", NORMAL)

        if verbosity >= NORMAL:
            self.stdout.write("=== Creating contact book for {} fake entities ===".format(n))

        command_start_time = time.time()

        # Do the job
        deng = DatabaseEngineer()

        for i in range(n):
            if verbosity >= NORMAL:
                self.stdout.write("=== Creating The Youbee Test Company ===")

            contact_book_start_time = time.time()
            deng.construct_contact_book(entity_id=i)

            if verbosity >= NORMAL:
                self.stdout.write("=== Created in %.2f seconds ===" % (time.time() - contact_book_start_time))

        if verbosity >= NORMAL:
            self.stdout.write("=== Done in %.2f seconds ===" % (time.time() - command_start_time))
