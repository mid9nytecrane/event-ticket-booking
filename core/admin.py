from django.contrib import admin
from .models import EventCategory,Event,Ticket,Organizer



admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Organizer)