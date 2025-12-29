from django.contrib import admin
from .models import EventCategory,Event,Ticket,Organizer,LikedEvent



admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Organizer)
admin.site.register(LikedEvent)