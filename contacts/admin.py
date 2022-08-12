# youbee_contacts/contacts/admin.py

# System libraries

# Third-party libraries

# Django modules
from django.contrib import admin

# Django apps
from .models import PersonGroup, PersonTitle, Person, PersonFunction, PhoneNumber, Location, EmailAddress, Organisation

#  Current app modules

admin.site.register(Person)
admin.site.register(PersonGroup)
admin.site.register(PersonTitle)
admin.site.register(PersonFunction)
admin.site.register(PhoneNumber)
admin.site.register(Location)
admin.site.register(EmailAddress)
admin.site.register(Organisation)




