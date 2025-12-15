from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid 
import qrcode
from io import BytesIO

# Create your models here.


class EventCategory(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = "Event Categories"

    def __str__(self) -> str:
        return self.name
    
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super(EventCategory, self).save()


class Event(models.Model):
    EVENT_TAG = {
        'paid': 'Paid',
        'free': 'Free'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True)
    category = models.ForeignKey(EventCategory, 
                                 on_delete=models.CASCADE, 
                                 related_name='events', null=True)
    event_tag = models.CharField(max_length=10, null=True, choices=EVENT_TAG, default="")
    organizer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=100)
    description = models.TextField(max_length=255 , blank=True)
    location = models.CharField(max_length=255)
    date = models.DateField()
    banner = models.ImageField(upload_to='event_banners/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    purchased_tickets = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):

        return f"{self.organizer}'s Event - <<{self.title}>>"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.event_tag == 'free':
            self.price = 0.00

        super(Event, self).save()

   




class Ticket(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchased_at = models.DateField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_used = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.event.title} - {self.attendee.username}"



class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer')
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    momo_numb = models.CharField(max_length=13)
    creator = models.BooleanField(default=False)


    def __str__(self):
        return f"Organizer - {self.full_name}({self.user})"





    
  