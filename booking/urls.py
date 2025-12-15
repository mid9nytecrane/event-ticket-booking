from django.urls import path 
from . import views 

app_name = 'booking'

urlpatterns = [
    path('event-ticket/<int:event_id>/', views.book_event, name='book-event'),
    path('my-tickets/', views.my_tickets, name='my-tickets'),
    path('verity-ticket/',views.verify_ticket, name='verify-ticket'),
]
