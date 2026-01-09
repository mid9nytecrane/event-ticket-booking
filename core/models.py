from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import uuid 
import qrcode
from io import BytesIO

from decimal import Decimal

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

    STATUS = {
        'active':'Active',
        'upcoming': 'Upcoming',
        'past': 'Past',
    }

    PAYMENT_STATUS = {
        'pending':'Pending',
        'paid': 'Paid',
    }
        

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True)
    category = models.ForeignKey(EventCategory, 
                                 on_delete=models.CASCADE, 
                                 related_name='events', null=True)
    event_tag = models.CharField(max_length=10, null=True, choices=EVENT_TAG, default="")
    organizer = models.CharField(max_length=255, null=True)
    likes = models.ManyToManyField(User, related_name="likes", through="LikedEvent")
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=100)
    description = models.TextField(max_length=255 , blank=True)
    location = models.CharField(max_length=255)
    date = models.DateField()
    banner = models.ImageField(upload_to='event_banners/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    purchased_tickets = models.PositiveIntegerField(blank=True, default=0)
    status = models.CharField(max_length=10,null=True,choices=STATUS,default='')
    payment_status = models.CharField(max_length=10, null=True, choices=PAYMENT_STATUS)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):

        return f"{self.organizer}'s Event - <<{self.title}>>"

    @property
    def is_free(self):
        return self.price == 0.00 or self.event_tag.lower() == 'free'
    
    @property
    def remaining_tickets(self):
        return self.total_tickets - self.purchased_tickets
    

    #number of likes count
    def number_of_likes(self):
        self.likes.count()
    

    def register_free_tickets(self):
        if not self.is_free:
            return False 
        
        if self.purchased_tickets >= self.total_tickets:
            return False 
        
        self.purchased_tickets += 1
        self.save()
        return True 
    

    

    
    @property
    def is_active(self):
        """check if the date is today """
        return self.date == timezone.now().date()
    
    @property
    def is_upcoming(self):
        """ check if the date is in the future"""
        return self.date > timezone.now().date()
    
    @property
    def is_past(self):
        return self.date < timezone.now().date()

    @property
    def total_purchased_tickets(self):
        if self.purchased_tickets is None:
            return 0
        return self.purchased_tickets

    @property
    def revenue(self):
        if self.purchased_tickets is None or self.price is None:
            return 0
        total = self.purchased_tickets * self.price
        revenue = Decimal('0.95') * total 
        return revenue
    
    @property
    def revenue_formatted(self):
        return f"GH₵ {self.revenue:.2f}"
    
    
    
    def save(self, *args, **kwargs):
        # Generate slug if not present
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set price to 0 if event is free
        if self.event_tag == 'free':
            self.price = Decimal('0.00')
        
        # Get current date for comparison
        current_date = timezone.now().date()
        
        # Determine and set status based on date comparison
        if self.date == current_date:
            self.status = 'active'
        elif self.date > current_date:
            self.status = 'upcoming'
        else:  # self.date < current_date
            self.status = 'past'
        
        # setting page field
        if self.is_paid:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'pending'
        
        super().save(*args, **kwargs)

   
#through table for events liked
class LikedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.event.title}"



class Ticket(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchased_at = models.DateField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_used = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.event.title} - {self.attendee.username}"



class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer')
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    momo_numb = models.CharField(max_length=13, null=True)
    creator = models.BooleanField(default=False)


    def __str__(self):
        return f"Organizer - {self.full_name}({self.user})"





    
  