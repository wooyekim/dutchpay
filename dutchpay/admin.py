from django.contrib import admin

from .models import Item, Consume, Meeting, Person, Place, Participation

admin.site.register(Item)
admin.site.register(Consume)
admin.site.register(Meeting)
admin.site.register(Place)
admin.site.register(Person)
admin.site.register(Participation)
